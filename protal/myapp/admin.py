from django.contrib import admin

from .models import Activity, AptitudeQuestion, AttemptAnswer, PrepTest, Resume, TestAttempt, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'phone', 'location')


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'ats_score', 'updated_at')
    search_fields = ('full_name', 'email', 'skills')


@admin.register(PrepTest)
class PrepTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'question_count', 'duration_minutes', 'is_active')
    list_filter = ('category', 'difficulty', 'is_active')
    search_fields = ('title', 'topics')


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'status', 'score', 'correct_answers', 'total_questions', 'started_at')
    list_filter = ('status', 'test__category')
    search_fields = ('user__username', 'test__title')


@admin.register(AptitudeQuestion)
class AptitudeQuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'order', 'topic', 'correct_option')
    list_filter = ('test__difficulty', 'topic')
    search_fields = ('question_text', 'topic', 'test__title')


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct')
    list_filter = ('is_correct', 'question__topic')
    search_fields = ('attempt__user__username', 'question__question_text')


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'status', 'created_at')
    search_fields = ('user__username', 'title', 'status')

# Register your models here.
