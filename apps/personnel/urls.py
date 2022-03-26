from django.urls import path, re_path

from helpers.constants import UUID_REGEX
from .views import (
    DashboardView,
    UserListView,
    UserDetailView,
    UsersDetailView,
    # user_detail_view,
    # users_detail_view,
    user_form_view,
    users_form_view,
    UserDeleteView,
    ContractListView,
    ContractDetailView,
    ContractCreateView,
    ContractUpdateView,
    ContractDeleteView,
    ContractCommentListView,
    ContractCommentDetailView,
    ContractCommentCreateView,
    ContractCommentUpdateView,
    ContractCommentDeleteView,
    role_form_view,
    assign_role_view,
)

app_name = 'personnel'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('users/', UserListView.as_view(), name='users'),
    path('user/detail/', UserDetailView.as_view(), name='user_detail'),
    path('users/detail/<int:id>', UsersDetailView.as_view(), name='users_detail'),
    path('user/form/', user_form_view, name='user_form'),
    path('users/form/<int:user_id>', users_form_view, name='users_form'),
    path('users/delete/<int:id>', UserDeleteView.as_view(), name='user_delete'),
    path('contracts/', ContractListView.as_view(), name='contracts'),
    path('contracts/<uuid:id>/', ContractDetailView.as_view(), name='contracts_detail'),
    path('contracts/form/<uuid:id>/', ContractUpdateView.as_view(), name='contracts_update'),
    path('contracts/form/', ContractCreateView.as_view(), name='contracts_form'),
    path('contract/delete/<uuid:id>', ContractDeleteView.as_view(), name='contract_delete'),
    path('contracts/comments/', ContractCommentListView.as_view(), name='contracts_comments'),
    path('contracts/comments/<uuid:id>/', ContractCommentDetailView.as_view(), name='contracts_comments_detail'),
    path('contracts/comments/form/<uuid:id>/', ContractCommentUpdateView.as_view(), name='contracts_comments_update'),
    path('contracts/comments/form/', ContractCommentCreateView.as_view(), name='contracts_comments_form'),
    path('contracts/comments/form/<uuid:id>/', ContractCommentUpdateView.as_view(), name='contracts_comments_update'),
    path('contracts/comments/delete/<uuid:id>/', ContractCommentDeleteView.as_view(), name='contracts_comments_update'),
    re_path(r'roles/form/(?P<role_id>(new|{})+)/'.format(UUID_REGEX), role_form_view, name='create_role_form'),
    path('roles/assign/form/', assign_role_view, name='assign_role_form'),
]
