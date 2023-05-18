from rest_framework import generics

from .serializers import UserRegisterSerializer
from .models import User


class AuthorCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
