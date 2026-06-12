from django import forms
from .models import Test

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['title', 'description', 'duration', 'total_marks']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter test title'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter test description',
                'rows': 4
            }),
            'duration': forms.NumberInput(attrs={
                'placeholder': 'Duration in minutes'
            }),
            'total_marks': forms.NumberInput(attrs={
                'placeholder': 'Total marks'
            }),
        }
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'