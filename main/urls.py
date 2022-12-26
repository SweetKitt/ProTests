from django.urls import path
from . import views


urlpatterns = [
    path('mygroupslist/', views.ManageGroupListView.as_view(), name='my_groups_list'),
    path('create/', views.GroupCreateView.as_view(), name='group_create'),
    path('<pk>/edit/', views.GroupUpdateView.as_view(), name='group_edit'),
    path('<pk>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),
    path('<pk>/groups/', views.GroupTestUpdateView.as_view(), name='group_test_update'),
    path('<pk>/tests/', views.TestQuestionUpdateView.as_view(), name='test_question_update'),
    path('test/<int:test_id>/', views.TestContentListView.as_view(), name='test_content_list'),
    path('test/order/', views.TestOrderView.as_view(), name='test_order'),
    path('question/order/', views.QuestionOrderView.as_view(), name='question_order'),
    path('question/<int:id>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
]