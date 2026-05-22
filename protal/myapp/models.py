from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Resume(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=120, blank=True)
    links = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    degree = models.CharField(max_length=180, blank=True)
    graduation = models.CharField(max_length=80, blank=True)
    ats_score = models.PositiveSmallIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name}'s resume"


class PrepTest(models.Model):
    APTITUDE = 'aptitude'
    CODING = 'coding'
    MOCK = 'mock'
    RESUME = 'resume'

    CATEGORY_CHOICES = [
        (APTITUDE, 'Aptitude'),
        (CODING, 'Coding'),
        (MOCK, 'Mock Test'),
        (RESUME, 'Resume'),
    ]

    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'

    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    ]

    title = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default=MEDIUM)
    question_count = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0)
    topics = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TestAttempt(models.Model):
    STARTED = 'started'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STARTED, 'Started'),
        (COMPLETED, 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(PrepTest, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STARTED)
    score = models.PositiveSmallIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    topic_breakdown = models.JSONField(default=dict, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.test.title}"


class AptitudeQuestion(models.Model):
    OPTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    test = models.ForeignKey(PrepTest, on_delete=models.CASCADE, related_name='aptitude_questions')
    order = models.PositiveIntegerField()
    topic = models.CharField(max_length=80)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    explanation = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['test', 'order'], name='unique_question_order_per_test'),
        ]

    def __str__(self):
        return f"{self.test.title} Q{self.order}"


class AttemptAnswer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(AptitudeQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1, blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['question__order']
        constraints = [
            models.UniqueConstraint(fields=['attempt', 'question'], name='unique_answer_per_question'),
        ]

    def __str__(self):
        return f"{self.attempt} - Q{self.question.order}"


class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=160)
    status = models.CharField(max_length=40, default='Completed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CodingQuestion(models.Model):
    test = models.ForeignKey(PrepTest, on_delete=models.CASCADE, related_name='coding_questions')
    order = models.PositiveIntegerField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=PrepTest.DIFFICULTY_CHOICES, default=PrepTest.MEDIUM)
    input_format = models.TextField(blank=True)
    output_format = models.TextField(blank=True)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    test_cases = models.JSONField(default=list, blank=True)  # List of dicts: [{"input": "...", "output": "..."}]

    # Starter codes
    starter_code_python = models.TextField(blank=True)
    starter_code_java = models.TextField(blank=True)
    starter_code_cpp = models.TextField(blank=True)
    starter_code_c = models.TextField(blank=True)
    starter_code_js = models.TextField(blank=True)

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['test', 'order'], name='unique_coding_question_order_per_test'),
        ]

    def __str__(self):
        return f"{self.test.title} - {self.title}"


class CodingSubmission(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='coding_submissions')
    question = models.ForeignKey(CodingQuestion, on_delete=models.CASCADE, related_name='submissions')
    language = models.CharField(max_length=20)
    code = models.TextField()
    status = models.CharField(max_length=40, default='Pending')  # 'Passed', 'Failed', 'Compile Error', etc.
    passed_cases = models.PositiveIntegerField(default=0)
    total_cases = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.title} ({self.status})"

