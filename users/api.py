from django.shortcuts import render, get_object_or_404
from django.views import View
from accounts.models import UserProfile
import json
from .serializers import UserProfileAPISerializer, UserProfileListSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser


class UserDetailAPI(RetrieveAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileAPISerializer
    lookup_field = 'pk'
    permission_classes = (IsAdminUser,)


class UserListAPI(ListAPIView):

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer
    permission_classes = (IsAdminUser,)
