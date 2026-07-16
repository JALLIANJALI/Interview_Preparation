from django.db import migrations


def create_sample_questions(apps, schema_editor):
    Category = apps.get_model('questions', 'Category')
    Question = apps.get_model('questions', 'Question')

    aptitude = Category.objects.get_or_create(name='Aptitude')[0]
    technical = Category.objects.get_or_create(name='Technical')[0]
    hr = Category.objects.get_or_create(name='HR')[0]

    sample_questions = [
        {
            'category': aptitude,
            'question_type': 'MCQ',
            'question_text': 'If 5x - 3 = 2x + 12, what is the value of x?',
            'option_a': '3',
            'option_b': '4',
            'option_c': '5',
            'option_d': '6',
            'correct_answer': 'C',
            'difficulty': 'Easy',
        },
        {
            'category': aptitude,
            'question_type': 'MCQ',
            'question_text': 'What is the next number in the series: 2, 6, 12, 20, ?.',
            'option_a': '24',
            'option_b': '28',
            'option_c': '30',
            'option_d': '32',
            'correct_answer': 'C',
            'difficulty': 'Easy',
        },
        {
            'category': aptitude,
            'question_type': 'MCQ',
            'question_text': 'A shop offers a 15% discount on a product priced at 400. What is the discount amount?',
            'option_a': '40',
            'option_b': '50',
            'option_c': '60',
            'option_d': '70',
            'correct_answer': 'C',
            'difficulty': 'Easy',
        },
        {
            'category': technical,
            'question_type': 'MCQ',
            'question_text': 'Which SQL statement is used to remove all records from a table without deleting the table itself?',
            'option_a': 'DELETE',
            'option_b': 'TRUNCATE',
            'option_c': 'DROP',
            'option_d': 'REMOVE',
            'correct_answer': 'B',
            'difficulty': 'Medium',
        },
        {
            'category': technical,
            'question_type': 'MCQ',
            'question_text': 'What is the time complexity of binary search on a sorted array?',
            'option_a': 'O(n)',
            'option_b': 'O(log n)',
            'option_c': 'O(n log n)',
            'option_d': 'O(1)',
            'correct_answer': 'B',
            'difficulty': 'Easy',
        },
        {
            'category': technical,
            'question_type': 'TEXT',
            'question_text': 'Name one HTTP method commonly used to update a resource.',
            'option_a': '',
            'option_b': '',
            'option_c': '',
            'option_d': '',
            'correct_answer': 'PUT',
            'difficulty': 'Medium',
        },
        {
            'category': hr,
            'question_type': 'TEXT',
            'question_text': 'How do you handle tight deadlines while maintaining quality work?',
            'option_a': '',
            'option_b': '',
            'option_c': '',
            'option_d': '',
            'correct_answer': 'By prioritizing tasks, communicating clearly, and focusing on high-impact work.',
            'difficulty': 'Easy',
        },
        {
            'category': hr,
            'question_type': 'MCQ',
            'question_text': 'If you disagree with your manager’s direction, what should you do?',
            'option_a': 'Ignore it and do your own work',
            'option_b': 'Share your concerns respectfully with facts',
            'option_c': 'Tell your coworkers about it',
            'option_d': 'Quit immediately',
            'correct_answer': 'B',
            'difficulty': 'Medium',
        },
        {
            'category': hr,
            'question_type': 'TEXT',
            'question_text': 'What is the first thing you do when joining a new team?',
            'option_a': '',
            'option_b': '',
            'option_c': '',
            'option_d': '',
            'correct_answer': 'Introduce yourself, learn about the team goals, and understand the expected workflow.',
            'difficulty': 'Easy',
        },
    ]

    for data in sample_questions:
        Question.objects.get_or_create(
            category=data['category'],
            question_text=data['question_text'],
            defaults={
                'question_type': data['question_type'],
                'option_a': data['option_a'],
                'option_b': data['option_b'],
                'option_c': data['option_c'],
                'option_d': data['option_d'],
                'correct_answer': data['correct_answer'],
                'difficulty': data['difficulty'],
            }
        )


def reverse_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_questions, reverse_func),
    ]
