from django.shortcuts import render, get_object_or_404
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from django.views import View
from accounts.models import UserProfile
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

from .serializers import UserProfileSerializer
from .forms import PasswordForm, PasswordWithPhoneForm
from django.urls import reverse, resolve
from .decorators import user_is_admin
from django.contrib.auth import update_session_auth_hash


class Home(View):

    def get(self, request):
        return HttpResponseRedirect('/accounts/login/')


class UserDetail(LoginRequiredMixin, DetailView):
    model = UserProfile

    def get_context_data(self, object):
        return UserProfileSerializer(object).data

    @user_is_admin
    def get(self, request, pk):
        userprofile = self.get_context_data(object=self.get_object())
        return render(request, 'users/userprofile_detail.html', {"userprofile": userprofile})


class UserList(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = "users/userprofile_list.html"


class UserSearch(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = "users/user_search.html"

    @user_is_admin
    def get_queryset(self, *args, **kwargs):
        phone_number = self.request.GET.get('phone_number')
        if phone_number:
            return UserProfile.objects.filter(phone_number=phone_number)
        return []


class SetPassword(LoginRequiredMixin, View):
    template_name = "users/set_password.html"

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        if not profile.phone_number:
            form = PasswordWithPhoneForm
        else:
            form = PasswordForm

        return render(request, self.template_name, {"form": form, "success": True if request.GET.get('success') else False})

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        if not profile.phone_number:
            form = PasswordWithPhoneForm(data=request.POST)
        else:
            form = PasswordForm(data=request.POST)
        if form.is_valid():
            profile.user.set_password(form.cleaned_data["password"])
            profile.user.save()
            if form.cleaned_data.get("phone_number"):
                profile.phone_number = form.cleaned_data["phone_number"]
                profile.save()
            update_session_auth_hash(request, profile.user)
            return HttpResponseRedirect('/accounts/profile/')
        return render(request, self.template_name, {"form": form})
