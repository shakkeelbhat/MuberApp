from .models import Passenger,Driver
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import exceptions







class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
   
class UserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']




class PassengerPatchSerializer(serializers.ModelSerializer):
    user = UserPatchSerializer()

    class Meta:
        model = Passenger
        fields = ['user', 'total_rides', 'age']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.age = validated_data.get('age', instance.age)
        instance.save()

        user_serializer = UserPatchSerializer(user, data=user_data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return instance


    

class PassengerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Passenger
        fields = ['user', 'age', 'total_rides']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        passenger = Passenger.objects.create(user=user, **validated_data)
        return passenger
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('password', None)
        return ret


class PassengerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if user:
                if user.is_active:
                    try:
                        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                        payload = jwt_payload_handler(user)
                        token = jwt_encode_handler(payload)
                        data["token"] = token
                    except Exception as e:
                        raise serializers.ValidationError("Error in generating token")
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with provided credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data


    def create(self, validated_data):
        return validated_data
    


class DriverSerializer(serializers.ModelSerializer):
    name = UserSerializer()

    class Meta:
        model = Driver
        fields = ['name', 'positive_likes', 'negative_likes', 'car_model', 'age', 'languages']
        read_only_fields = ['positive_likes', 'negative_likes']

    def create(self, validated_data):
        user_data = validated_data.pop('name')
        #user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        user = User.objects.create_user(**user_data)

        driver = Driver.objects.create(name=user, **validated_data)
        return driver



class DriverLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:

            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if user:
                if user.is_active:
                    try:
                        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

                        payload = jwt_payload_handler(user)
                        token = jwt_encode_handler(payload)
                        data["token"] = token
                    except Exception as e:
                        raise serializers.ValidationError("Error in generating token")
                else:
                    msg = "User is deactivated."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with provided credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data





class DriverPatchSerializer(serializers.ModelSerializer):
    name = UserPatchSerializer()

    class Meta:
        model = Driver
        fields = ['name', 'car_model', 'age','languages']
        read_only_fields = ['positive_likes', 'negative_likes']

    def update(self, instance, validated_data):
        try:
            user_data = validated_data.get('name',instance)
            name = instance.name
            instance.car_model = validated_data.get('car_model', instance.car_model)

            instance.age = validated_data.get('age', instance.age)
            instance.languages = validated_data.get('languages', instance.languages)
            instance.save()

            user_serializer = UserPatchSerializer(name, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        except:
            Exception("provided field should include 'name")
       
        return instance