from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .decorators import required_permissions, RequiredPermissionsMixin
from .forms import (
    UserForm,
    ProfileInlineFormset,
    BankInlineFormset,
    EducationInlineFormset,
    SpouseInlineFormset,
    ChildInlineFormset,
    ContractForm,
    ContractCommentForm,
    RoleForm,
    AssignRoleForm,
)
from .models import Profile, Contract, Role, Permission, ContractComment

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'personnel/dashboard.html'


class UserListView(LoginRequiredMixin, RequiredPermissionsMixin, ListView):
    model = User
    template_name = 'personnel/user_list.html'
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions '

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context.update(
            {
                'profile': Profile.objects.all(),
                'contract': Contract.objects.all(),
            }
        )
        return context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'personnel/user_detail.html'

    def get_object(self, *args, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        context['profiles'] = self.object.profiles
        context['educations'] = self.object.educations.filter(user_id=self.request.user)
        context['banks'] = self.object.banks.filter(user_id=self.request.user)
        context['spouses'] = self.object.spouses.filter(user_id=self.request.user)
        context['children'] = self.object.children.filter(user_id=self.request.user)
        return context


class UsersDetailView(LoginRequiredMixin, RequiredPermissionsMixin, DetailView):
    model = User
    template_name = 'personnel/user_detail.html'
    pk_url_kwarg = 'id'
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]

    def get_context_data(self, **kwargs):
        context = super(UsersDetailView, self).get_context_data()
        context['profiles'] = self.object.profiles
        context['educations'] = self.object.educations.filter()
        context['banks'] = self.object.banks.filter()
        context['spouses'] = self.object.spouses.filter()
        context['children'] = self.object.children.filter()
        return context


@require_http_methods(['GET', 'POST'])
def _generic_user_form_view(request, query=None):
    if request.user.is_authenticated:
        instance = query.get()
        user_form = UserForm(instance=instance)
        profile_form = ProfileInlineFormset(instance=instance)
        bank_form = BankInlineFormset(instance=instance)
        education_form = EducationInlineFormset(instance=instance)
        spouse_form = SpouseInlineFormset(instance=instance)
        child_form = ChildInlineFormset(instance=instance)
    else:
        user_form = UserForm()
        profile_form = ProfileInlineFormset()
        bank_form = BankInlineFormset()
        education_form = EducationInlineFormset()
        spouse_form = SpouseInlineFormset()
        child_form = ChildInlineFormset()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileInlineFormset(request.POST, request.FILES)
        bank_form = BankInlineFormset(request.POST)
        education_form = EducationInlineFormset(request.POST, request.FILES)
        spouse_form = SpouseInlineFormset(request.POST, request.FILES)
        child_form = ChildInlineFormset(request.POST, request.FILES)

        if all(
            [
                user_form.is_valid(),
                profile_form.is_valid(),
                bank_form.is_valid(),
                education_form.is_valid(),
                spouse_form.is_valid(),
                child_form.is_valid(),
            ]
        ):
            user = user_form.save()

            profile_form.instance = user
            profile_form.save()

            bank_form.instance = user
            bank_form.save()

            education_form.instance = user
            education_form.save()

            spouse_form.instance = user
            spouse_form.save()

            child_form.instance = user
            child_form.save()

            return HttpResponseRedirect(reverse(settings.DASHBOARD_REDIRECT_URL))

    return render(
        request,
        'personnel/register.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'bank_form': bank_form,
            'education_form': education_form,
            'spouse_form': spouse_form,
            'child_form': child_form,
        },
    )


def user_form_view(request):
    if User.objects.filter(national_id__isnull=False) and request.user.is_authenticated:
        return redirect('personnel:dashboard')
    else:
        query = (
            User.objects.select_related('profiles')
            .prefetch_related(
                'banks',
                'educations',
                'spouses',
                'children',
            )
            .filter(id=request.user.id)
        )
        return _generic_user_form_view(request, query)


@required_permissions(
    [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
)
def users_form_view(request, user_id):
    query = (
        User.objects.select_related('profiles')
        .prefetch_related(
            'banks',
            'educations',
            'spouses',
            'children',
        )
        .filter(id=user_id)
    )
    return _generic_user_form_view(request, query)


class UserDeleteView(LoginRequiredMixin, RequiredPermissionsMixin, SuccessMessageMixin, DeleteView):
    model = User
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('personnel:dashboard')
    success_message = _('User deleted successfully')
    permission_required = [[Permission.Codes.ACCEPT_DELETE_DEMAND], [Permission.Codes.ALL_PERMISSION]]
    permission_denied_message = 'no required permissions '
    template_name = 'personnel/user_confirm_delete.html'


class ContractListView(LoginRequiredMixin, RequiredPermissionsMixin, ListView):
    model = Contract
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions '


class ContractDetailView(LoginRequiredMixin, RequiredPermissionsMixin, DetailView):
    model = Contract
    slug_url_kwarg = 'id'
    slug_field = 'id'
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions '


class ContractCreateView(LoginRequiredMixin, RequiredPermissionsMixin, SuccessMessageMixin, CreateView):
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy('personnel:dashboard')
    success_message = _('Contract created successfully')
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions '


class ContractUpdateView(LoginRequiredMixin, RequiredPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = Contract
    slug_url_kwarg = 'id'
    slug_field = 'id'
    form_class = ContractForm
    success_url = reverse_lazy('personnel:dashboard')
    success_message = _('Contract updated successfully')
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions '


class ContractDeleteView(LoginRequiredMixin, RequiredPermissionsMixin, SuccessMessageMixin, DeleteView):
    model = Contract
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('personnel:dashboard')
    success_message = _('Contract deleted successfully')
    permission_required = [[Permission.Codes.ACCEPT_DELETE_DEMAND], [Permission.Codes.ALL_PERMISSION]]
    permission_denied_message = 'no required permissions '


class ContractCommentListView(LoginRequiredMixin, RequiredPermissionsMixin, ListView):
    model = ContractComment
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions '


class ContractCommentDetailView(RequiredPermissionsMixin, DetailView):
    model = ContractComment
    slug_url_kwarg = 'id'
    slug_field = 'id'
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions '


class ContractCommentCreateView(LoginRequiredMixin, RequiredPermissionsMixin, SuccessMessageMixin, CreateView):
    model = ContractComment
    form_class = ContractCommentForm
    success_url = reverse_lazy('personnel:dashboard')
    success_message = _('Your comments sent successfully')
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions'


class ContractCommentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ContractComment
    slug_url_kwarg = 'id'
    slug_field = 'id'
    form_class = ContractCommentForm
    success_url = reverse_lazy('personnel:dashboard')
    success_message = _('Your comments updated successfully')
    permission_required = [
        [Permission.Codes.VIEW_AND_CHANGE_USERS_DATA, Permission.Codes.ACCEPT_DEMAND_FOR_CHANGE_USERS_DATA],
        [Permission.Codes.ALL_PERMISSION],
    ]
    permission_denied_message = 'no required permissions '


class ContractCommentDeleteView(LoginRequiredMixin, RequiredPermissionsMixin, SuccessMessageMixin, DeleteView):
    model = ContractComment
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('personnel:dashboard')
    success_message = _('Comment deleted successfully')
    permission_required = [[Permission.Codes.ACCEPT_DELETE_DEMAND], [Permission.Codes.ALL_PERMISSION]]
    permission_denied_message = 'no required permissions '


@login_required
@required_permissions([[Permission.Codes.ALL_PERMISSION]])
@require_http_methods(['GET', 'POST'])
def role_form_view(request, role_id):
    if role_id == 'new':
        form = RoleForm()
    else:
        obj = get_object_or_404(Role, id=role_id)
        data = {'title': obj.title, 'codes': [permission.code for permission in obj.permissions.all()]}
        form = RoleForm(data=data)

    if request.method == 'POST':
        form = RoleForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            codes = form.cleaned_data['codes']
            role = Role.objects.create(title=title)
            for code in codes:
                Permission.objects.create(code=code, role=role)

        return redirect('personnel:assign_role_form')

    return render(request, 'personnel/create_roles.html', {'form': form})


@login_required
@required_permissions([[Permission.Codes.ALL_PERMISSION]])
@require_http_methods(['GET', 'POST'])
def assign_role_view(request):
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role_titles = form.cleaned_data['role_titles']
            users = form.cleaned_data['users']
            role = Role.objects.get(title=role_titles)
            role.users.add(users)

        return redirect('personnel:dashboard')

    return render(request, 'personnel/assign_roles.html', {'form': form})
