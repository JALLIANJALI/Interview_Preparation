from django.db import models
from django.contrib.auth.models import User
from questions.models import Question
from django.utils import timezone

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    session = models.ForeignKey(
        'InterviewSession',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='answers'
    )
    answer = models.TextField()

    is_correct = models.BooleanField(default=False)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.question_text[:30]}"  

class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True,blank=True)

    def score(self):
        return self.answers.filter(is_correct=True).count()

    def total(self):
        return self.answers.count()

    def duration(self):
        if not self.completed_at:
            return None
        return self.completed_at - self.started_at

    def __str__(self):
        return f"{self.user.username} - {self.started_at.strftime('%d-%m-%y %H:%M')}" 
    