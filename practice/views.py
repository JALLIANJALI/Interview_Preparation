from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from questions.models import Question, Category
from .models import UserAnswer, InterviewSession
from django.utils import timezone

SECTION_SLUG_TO_NAME = {
    'aptitude': 'Aptitude',
    'technical': 'Technical',
    'hr': 'HR',
}

# per-section time limits in seconds (editable)
SECTION_TIMES = {
    'aptitude': 10 * 60,   # 10 minutes
    'technical': 20 * 60,  # 20 minutes
    'hr': 10 * 60,         # 10 minutes
}

# overall interview time in seconds (editable)
OVERALL_TIME = 40 * 60  # 40 minutes


def get_or_create_session(request):
    session_id = request.session.get('interview_session_id')
    session_obj = None
    if session_id:
        try:
            session_obj = InterviewSession.objects.get(id=session_id, user=request.user)
        except InterviewSession.DoesNotExist:
            session_obj = None

    if not session_obj:
        session_obj = InterviewSession.objects.create(user=request.user)
        request.session['interview_session_id'] = session_obj.id

    return session_obj


def start_section(request, category_slug):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    category_name = SECTION_SLUG_TO_NAME.get(category_slug)
    if not category_name:
        messages.error(request, "Unknown section.")
        return redirect('dashboard')

    category, _ = Category.objects.get_or_create(name=category_name)

    # Show a start confirmation page on GET; only initialize timers and redirect on POST
    if request.method != 'POST':
        # compute remaining overall time if already initialized
        from django.utils import timezone as _tz
        now_ts = _tz.now().timestamp()
        overall_deadline = request.session.get('interview_deadline')
        overall_remaining = None
        if overall_deadline:
            overall_remaining = max(0, int(overall_deadline - now_ts))

        sec_seconds = SECTION_TIMES.get(category_slug, 10 * 60)
        # precompute minutes/seconds to avoid template arithmetic
        section_minutes = sec_seconds // 60
        section_seconds_remainder = sec_seconds % 60

        overall_minutes = None
        overall_seconds_remainder = None
        if overall_remaining is not None:
            overall_minutes = overall_remaining // 60
            overall_seconds_remainder = overall_remaining % 60

        return render(request, 'section_start.html', {
            'category_name': category_name,
            'category_slug': category_slug,
            'section_seconds': sec_seconds,
            'section_minutes': section_minutes,
            'section_seconds_remainder': section_seconds_remainder,
            'overall_remaining': overall_remaining,
            'overall_minutes': overall_minutes,
            'overall_seconds_remainder': overall_seconds_remainder,
        })

    # POST: actually start the section
    session_obj = get_or_create_session(request)

    # initialize overall interview deadline once per interview
    from django.utils import timezone as _tz
    from datetime import timedelta
    if not request.session.get('interview_deadline'):
        request.session['interview_deadline'] = (
            (_tz.now() + timedelta(seconds=OVERALL_TIME)).timestamp()
        )

    # set section deadline when starting a section
    sec_seconds = SECTION_TIMES.get(category_slug, 10 * 60)
    request.session['section_deadline'] = (
        (_tz.now() + timedelta(seconds=sec_seconds)).timestamp()
    )
    request.session['current_section_slug'] = category_slug

    next_question = Question.objects.filter(category=category).exclude(
        useranswer__session=session_obj
    ).order_by('id').first()

    if not next_question:
        messages.info(request, f"No questions available in {category_name}. Please add questions in admin.")
        return redirect('dashboard')

    next_url = reverse('practice', kwargs={'question_id': next_question.id})
    return redirect(f"{next_url}?section={category_slug}")


def practice(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    session_obj = get_or_create_session(request)
    category_slug = request.GET.get('section')
    category_name = SECTION_SLUG_TO_NAME.get(category_slug) if category_slug else None
    category = None
    if category_name:
        category, _ = Category.objects.get_or_create(name=category_name)

    # compute remaining times (in seconds) for section and overall
    from django.utils import timezone as _tz
    import time
    now_ts = _tz.now().timestamp()
    overall_deadline = request.session.get('interview_deadline')
    section_deadline = request.session.get('section_deadline')
    overall_remaining = None
    section_remaining = None
    if overall_deadline:
        overall_remaining = max(0, int(overall_deadline - now_ts))
    if section_deadline:
        section_remaining = max(0, int(section_deadline - now_ts))

    if request.method == "POST":
        user_answer = request.POST.get("answer", "")
        is_correct = (
            user_answer.strip().lower()
            == question.correct_answer.strip().lower()
        )

        UserAnswer.objects.create(
            user=request.user,
            question=question,
            session=session_obj,
            answer=user_answer,
            is_correct=is_correct
        )

        question_qs = Question.objects.filter(category=category) if category else Question.objects.all()
        next_question = question_qs.exclude(
            useranswer__session=session_obj
        ).order_by('id').first()

        if next_question:
            next_url = reverse('practice', kwargs={'question_id': next_question.id})
            if category_slug:
                next_url = f"{next_url}?section={category_slug}"
            return redirect(next_url)

        session_obj.completed_at = timezone.now()
        session_obj.save()
        try:
            del request.session['interview_session_id']
        except KeyError:
            pass

        answer_filter = session_obj.answers
        if category:
            answer_filter = answer_filter.filter(question__category=category)

        total = answer_filter.count()
        score = answer_filter.filter(is_correct=True).count()
        wrong_answers = total - score

        return render(request, "result.html", {
            "total": total,
            "score": score,
            "wrong_answers": wrong_answers,
            "category_name": category_name,
        })

    if session_obj.answers.filter(question=question).exists():
        question_qs = Question.objects.filter(category=category) if category else Question.objects.all()
        next_question = question_qs.exclude(
            useranswer__session=session_obj
        ).order_by('id').first()

        if next_question:
            next_url = reverse('practice', kwargs={'question_id': next_question.id})
            if category_slug:
                next_url = f"{next_url}?section={category_slug}"
            return redirect(next_url)
        return redirect('dashboard')

    return render(request, "practice.html", {
        "question": question,
        "category_name": category_name,
        "section_remaining": section_remaining,
        "overall_remaining": overall_remaining,
        "current_section_slug": category_slug,
    })


def end_interview(request):
    # End the current interview session and show aggregated results
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    session_id = request.session.get('interview_session_id')
    if not session_id:
        return redirect('dashboard')

    try:
        session_obj = InterviewSession.objects.get(id=session_id, user=request.user)
    except InterviewSession.DoesNotExist:
        return redirect('dashboard')

    # compute overall results
    answer_filter = session_obj.answers
    total = answer_filter.count()
    score = answer_filter.filter(is_correct=True).count()
    wrong_answers = total - score

    session_obj.completed_at = timezone.now()
    session_obj.save()

    # clear deadlines
    for k in ('interview_deadline', 'section_deadline', 'interview_session_id', 'current_section_slug'):
        try:
            del request.session[k]
        except Exception:
            pass

    return render(request, 'result.html', {
        'total': total,
        'score': score,
        'wrong_answers': wrong_answers,
        'category_name': None,
    })
  