from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):

    QUESTION_TYPES = [
        ('MCQ', 'Multiple Choice'),
        ('TEXT', 'Text Answer'),
    ]

    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default='MCQ'
    )

    question_text = models.TextField()

    option_a = models.CharField(max_length=255, blank=True)
    option_b = models.CharField(max_length=255, blank=True)
    option_c = models.CharField(max_length=255, blank=True)
    option_d = models.CharField(max_length=255, blank=True)

    correct_answer = models.CharField(max_length=255)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default='Easy'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:50] 