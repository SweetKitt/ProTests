from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')

    class Meta:
        ordering = ['title']
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.title


class Group(models.Model):
    owner = models.ForeignKey(User, related_name='owner_group', on_delete=models.CASCADE, verbose_name='Автор')
    subject = models.ForeignKey(Subject, related_name='subject_group', on_delete=models.CASCADE, verbose_name='Тема набора тестов')
    title = models.CharField(max_length=200, verbose_name='Название набора')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    overview = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Test(models.Model):
    group = models.ForeignKey(Group, related_name='group_test', on_delete=models.CASCADE, verbose_name='Набор тестов')
    title = models.CharField(max_length=200, verbose_name='Название теста')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='test_question', on_delete=models.CASCADE, verbose_name='Тест')
    question = models.TextField(verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='question_answer', on_delete=models.CASCADE, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    correct_answer = models.BooleanField(verbose_name='Правильный ответ')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Result(models.Model):
    test = models.ForeignKey(Test, verbose_name='Тест', on_delete=models.CASCADE)
    user = models.CharField(max_length=300, verbose_name="ФИО")
    DateTime = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Время завершения")
    Rating =models.FloatField(verbose_name="Проценты")