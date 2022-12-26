from django.contrib import admin
from .models import Subject, Group, Test, Question, Answer


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_filter = ['subject']
    prepopulated_fields = {'slug': ('title',)}


class AnswerInline(admin.StackedInline):
    model = Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'question']
    inlines = [AnswerInline]


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'group']
    list_filter = ['group']



