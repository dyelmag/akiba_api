from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from .models import Perfil


class UserSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(
        required=True, allow_blank=False, max_length=30)
    last_name = serializers.CharField(
        required=True, allow_blank=False, max_length=150)
    email = serializers.CharField(
        required=True, allow_blank=False)
    password = serializers.CharField(
        required=True, allow_blank=False)

    def create(self, validated_data):

        if User.objects.filter(email=validated_data['email']):
            raise serializers.ValidationError({
                "email": [
                    "Email ja cadastrado"
                ]})
        validated_data['username'] = validated_data['email']
        user = User.objects.create(**validated_data)
        # Cria perfil
        Perfil.objects.create(user=user)
        # encripta a senha
        user.set_password(validated_data['password'])
        user.save()
        return user


class PerfilSerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    profile_picture = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False)
    gender = serializers.IntegerField(required=False)
    date_of_birth = serializers.DateField(required=False)
    biography = serializers.CharField(max_length=400, required=False)

    def update(self, instance, validated_data):

        instance.profile_picture = validated_data.get(
            'profile_picture', instance.profile_picture)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get(
            'date_of_birth', instance.date_of_birth)
        instance.biography = validated_data.get(
            'biography', instance.biography)
        instance.save()
        return instance

    def create(self, validated_data):

        return Perfil.objects.create(**validated_data)
