from django.shortcuts import redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.urls import reverse_lazy
from .models import Group, Test, Question, Answer
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import ModuleFormSetGroup, ModuleFormSetQuestion
from django.apps import apps
from braces.views import CsrfExemptMixin, JSONResponseMixin


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerGroupMixin(OwnerMixin, LoginRequiredMixin):
    model = Group
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('my_groups_list')


class OwnerGroupEditMixin(OwnerGroupMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('my_groups_list')
    template_name = 'main/manage/groups/form.html'


class ManageGroupListView(OwnerGroupMixin, ListView):
    template_name = 'main/manage/groups/list.html'


class GroupCreateView(PermissionRequiredMixin, OwnerGroupEditMixin, CreateView):
    permission_required = 'main.add_group'


class GroupUpdateView(PermissionRequiredMixin, OwnerGroupEditMixin, UpdateView):
    permission_required = 'main.change_group'


class GroupDeleteView(PermissionRequiredMixin, OwnerGroupMixin, DeleteView):
    template_name = 'main/manage/groups/delete.html'
    success_url = reverse_lazy('my_groups_list')
    permission_required = 'main.delete_group'


class GroupTestUpdateView(TemplateResponseMixin, View):
    template_name = 'main/manage/tests/formset.html'
    group = None

    def get_formset(self, data=None):
        return ModuleFormSetGroup(instance=self.group, data=data)

    def dispatch(self, request, pk):
        self.group = get_object_or_404(Group,
                                        id=pk,
                                        owner=request.user)
        return super(GroupTestUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'group': self.group,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('my_groups_list')
        return self.render_to_response({'group': self.group,
                                        'formset': formset})


class TestQuestionUpdateView(TemplateResponseMixin, View):
    template_name = 'main/manage/questions/formset.html'
    question = None

    def get_formset(self, data=None):
        return ModuleFormSetQuestion(instance=self.question, data=data)

    def dispatch(self, request, pk):
        self.question = get_object_or_404(Question, id=pk,)
        return super(TestQuestionUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'question': self.question, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('my_groups_list')
        return self.render_to_response({'question': self.question,'formset': formset})


class TestContentListView(TemplateResponseMixin, View):
    template_name = 'main/manage/tests/content_list.html'

    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id, group__owner=request.user)
        return self.render_to_response({'test': test})


class TestOrderView(ConnectionRefusedError, JSONResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Test.objects.filter(id=id).update(order=order)
        return self.render_json_response({'saved':'ОК'})


class QuestionOrderView(CsrfExemptMixin, JSONResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Question.objects.filter(id=id).update(order=order)
        return self.render_json_response({'saved':'ОК'})


class QuestionDeleteView(View):
    def post(self, request, id):
        question = get_object_or_404(Question,
                                    id=id,
                                    test__group__owner=request.user)
        test = question.test
        question.delete()
        return redirect('test_content_list', test.id)

class QuestionCreateView(CreateView):
    permission_required = 'courses.add_course'


class QuestionUpdateView(UpdateView):
    permission_required = 'courses.change_course'