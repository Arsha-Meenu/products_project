from .models import CustomUser
from rest_framework import serializers
from phonenumber_field.serializerfields import  PhoneNumberField




class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False,allow_blank = False)
    password = serializers.CharField(min_length = 8,write_only = True)

    class Meta:
        model = CustomUser
        fields = ['username','email','phone_number','password']


    def validate(self,attrs):
        username_exists = CustomUser.objects.filter(username = attrs['username']).exists()
        if username_exists:
            raise serializers.ValidationError(detail = 'User with Username exists.')

        email_exists = CustomUser.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise serializers.ValidationError(detail='User with Email exists.')

        phonenumber_exists = CustomUser.objects.filter(phone_number=attrs['phone_number']).exists()
        if phonenumber_exists:
            raise serializers.ValidationError(detail='User with Phone Number exists.')
        
        return super().validate(attrs)


    def create(self,validated_data):
        user = CustomUser.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            password = validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user