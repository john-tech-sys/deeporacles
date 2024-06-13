
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import User
from contrib.permissions import IsAuthenticatedOrCreateOnly
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .serializers import UserSerializer


class UserViewset(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrCreateOnly]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination

