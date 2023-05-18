from rest_framework import serializers

from .models import Author, User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        return data

    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError('Пароль должен быть длиннее 8 символов')
        if not any(value.isdigit() for value in password):
            raise serializers.ValidationError('В пароле должны присутсвовать цифры')
        if not any(value.isupper() for value in password):
            raise serializers.ValidationError('В пароле должны быть заглавные буквы')
        if not any(value.islower() for value in password):
            raise serializers.ValidationError('В пароле должны быть прописные буквы')
        if not any(value in '!@#$%^&*()_-[]{}<>' for value in password):
            raise serializers.ValidationError('В пароле должны быть спецсимволы')
        return password

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        try:
            author = Author.objects.create(
                user=user
            )
        except Exception as e:
            user.delete()
            raise e
        else:
            author.username = user.username
        return author
