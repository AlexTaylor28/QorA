from django import forms
from .models import Question, Answer, Topic

class QuestionForm(forms.ModelForm):

    topics = forms.ModelMultipleChoiceField(
        queryset = Topic.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False,
        help_text = "Select topics relevant to your question."
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'topics']
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'content': forms.Textarea(attrs = {'class': 'form-control', 'rows': 5}),
        }
    

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Write your answer here...'
            }),
        }
        labels = {
            'content': ''
        }