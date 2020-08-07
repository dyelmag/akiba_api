from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework import mixins, generics
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .serializers import UserSerializer, PerfilSerializer
from .models import Perfil

# Create your views here.


class NewUserView(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = UserSerializer
    model = User
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PerfilView(mixins.UpdateModelMixin, generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = PerfilSerializer
    model = Perfil
    queryset = Perfil.objects.all()

    def get_object(self):
        user = self.request.user
        try:
            return Perfil.objects.get(user=user)
        except Perfil.DoesNotExist:
            raise Http404

    def get(self, request):
        print(request)
        serializer = PerfilSerializer(self.get_object())
        return Response(serializer.data)

    def put(self, request):
        return self.update(request)


class LoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
