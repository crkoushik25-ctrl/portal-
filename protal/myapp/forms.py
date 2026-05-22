from django import forms

from .models import AptitudeQuestion, PrepTest, CodingQuestion


class PrepTestForm(forms.ModelForm):
    class Meta:
        model = PrepTest
        fields = ['title', 'category', 'difficulty', 'question_count', 'duration_minutes', 'topics', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Test title'}),
            'question_count': forms.NumberInput(attrs={'min': 0}),
            'duration_minutes': forms.NumberInput(attrs={'min': 0}),
            'topics': forms.TextInput(attrs={'placeholder': 'Numbers, reasoning, DSA'}),
        }


class AptitudeQuestionForm(forms.ModelForm):
    class Meta:
        model = AptitudeQuestion
        fields = [
            'test',
            'order',
            'topic',
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_option',
            'explanation',
        ]
        widgets = {
            'order': forms.NumberInput(attrs={'min': 1}),
            'topic': forms.TextInput(attrs={'placeholder': 'Quantitative'}),
            'question_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter the question'}),
            'option_a': forms.TextInput(attrs={'placeholder': 'Option A'}),
            'option_b': forms.TextInput(attrs={'placeholder': 'Option B'}),
            'option_c': forms.TextInput(attrs={'placeholder': 'Option C'}),
            'option_d': forms.TextInput(attrs={'placeholder': 'Option D'}),
            'explanation': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Short solution or explanation'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test'].queryset = PrepTest.objects.filter(category=PrepTest.APTITUDE).order_by('difficulty', 'title')


class CodingQuestionForm(forms.ModelForm):
    class Meta:
        model = CodingQuestion
        fields = [
            'test',
            'order',
            'title',
            'description',
            'difficulty',
            'input_format',
            'output_format',
            'sample_input',
            'sample_output',
            'test_cases',
            'starter_code_python',
            'starter_code_java',
            'starter_code_cpp',
            'starter_code_c',
            'starter_code_js',
        ]
        widgets = {
            'order': forms.NumberInput(attrs={'min': 1}),
            'title': forms.TextInput(attrs={'placeholder': 'Problem title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Problem description'}),
            'input_format': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Input format'}),
            'output_format': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Output format'}),
            'sample_input': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Sample input'}),
            'sample_output': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Sample output'}),
            'test_cases': forms.Textarea(attrs={'rows': 3, 'placeholder': '[{"input": "...", "output": "..."}]'}),
            'starter_code_python': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python starter code'}),
            'starter_code_java': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Java starter code'}),
            'starter_code_cpp': forms.Textarea(attrs={'rows': 3, 'placeholder': 'C++ starter code'}),
            'starter_code_c': forms.Textarea(attrs={'rows': 3, 'placeholder': 'C starter code'}),
            'starter_code_js': forms.Textarea(attrs={'rows': 3, 'placeholder': 'JavaScript starter code'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test'].queryset = PrepTest.objects.filter(category=PrepTest.CODING).order_by('difficulty', 'title')
