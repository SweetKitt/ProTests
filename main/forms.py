from django import forms
from django.forms.models import inlineformset_factory
from .models import Group, Test, Question, Answer


ModuleFormSetGroup = inlineformset_factory(Group, Test, fields=['title', 'description'], extra=2, can_delete=True)
ModuleFormSetQuestion = inlineformset_factory(Question, Answer, fields=['question', 'answer', 'correct_answer'], extra=1, can_delete=True)