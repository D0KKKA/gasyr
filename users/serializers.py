from rest_framework import serializers
from users import models



class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Phone
        fileds="__all__"



class UserSerializer(serializers.ModelSerializer):
   # phone = PhoneSerializer()
    class Meta:
        model = models.User
        fields=(
            'id',
            'email',
            'first_name',
            'last_name',
            #'phone', хз че с ним ,при отправке данных ругается
        )