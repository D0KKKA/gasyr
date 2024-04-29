from rest_framework import serializers
from users import models







class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields="__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat',
            'phone',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data.get('password_repeat'):
            raise serializers.ValidationError("Пароли не совпадают")
        return data
    def create(self, validated_data):
        user = models.User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone = validated_data['phone']
        )
        user.set_password(validated_data['password'])

        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = models.User.objects.filter(email=email).first()
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to login with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'image',  'date_of_birth']



class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notifications
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notes
        fields = '__all__'