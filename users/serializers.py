from rest_framework import serializers
from users import models



class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phone
        fields="__all__"



class UserSerializer(serializers.ModelSerializer):
    phone = PhoneSerializer()
    class Meta:
        model = models.User
        fields="__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)
    class Meta:
        model=models.User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'phone_number',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', None)
        user = models.User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        if phone_number:
            models.Phone.objects.create(phone_number=phone_number, user=user)
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




