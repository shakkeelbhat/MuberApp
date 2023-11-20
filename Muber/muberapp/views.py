from .permissions import IsPremiumPassenger
from rest_framework import status
from .models import Driver,Passenger
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.models import User

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import PassengerSerializer, PassengerPatchSerializer,DriverSerializer,DriverLoginSerializer, PassengerLoginSerializer,DriverPatchSerializer





class HomeView(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self,request):
        message='Welcome to Muber app! If you are a drivers or a passengers, register to get the best of the app.'
        instructions ={'Endpoints':{'passengerRegister':'passengers/register/','passengerLogin':'passengers/login/','passengerDetails(get or patch)':'passengers/detail/','getDriverList':'passengers/drivers/','addDriverLikeDislike':'passengers/like/','driverRegister':'drivers/register/','driverLogin':'drivers/login/','driverUpdate(get or patch':'drivers/detail/'}}
        return Response({'message':message,'instructions':instructions},status=status.HTTP_200_OK)
    

class PassengerRegister(APIView):
    authentication_classes = []
    permission_classes = []


    def post(self, request, format=None):
        serializer = PassengerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data.pop('password', None)  # Remove password from the response
            data['message'] = f" Welcome passenger {data['user']['username']}! You have been registered successfully."
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PassengerLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        serializer = PassengerLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = User.objects.get(username=username)
            passenger = Passenger.objects.get(user=user)
            passenger.total_rides += 1
            passenger.save()
            return Response({'message': f'User with username {username} logged in.', 'token': serializer.validated_data.get('token')}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid data. Please provide valid data for login.'}, status=status.HTTP_400_BAD_REQUEST)

class PassengerDetail(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        passenger = Passenger.objects.get(user=request.user)
        serializer = PassengerSerializer(passenger)
        return Response(serializer.data)

    def patch(self, request, format=None):
        try:
            passenger = Passenger.objects.get(user=request.user)
        except Passenger.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.data:
            serializer = PassengerPatchSerializer(passenger, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PassengerPatchSerializer(passenger)
            return Response(serializer.data)

class DriverList(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = []

    def get(self, request, format=None):
        drivers = Driver.objects.all()
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)



class ChangeDriverLike(APIView):
    authentication_classes = [JSONWebTokenAuthentication]

    permission_classes = [IsPremiumPassenger]

    def post(self, request, format=None):
        try:
            
            driver = Driver.objects.get(name__username=request.data['username'])
            print(driver,'foinf')
            if 'like' in request.data and 'dislike' in request.data:
                return Response({"message":"expects {'username':'****','like':'+' or 'dislike':'-' }"})

            if request.data.get('like')=='+':
                driver.positive_likes += 1
            elif request.data.get('dislike')=='-':
                driver.negative_likes += 1
            driver.save()
            return Response({'message':f"Driver [{request.data['username']}] like/dislike updated"},status=status.HTTP_200_OK)
        except:
            return Response({"message":"expects {'username':'****','like':'+' or 'dislike':'-' }"})



class DriverRegister(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            driver = serializer.save()
            data = serializer.data
            data['message'] = f"Welcome driver [{data['name']['username']}]! You have been registered successfully with the following details: Age: {data['age']} Car Model: {data['car_model']} Languages: {data['languages']}"
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class DriverLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        serializer = DriverLoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            username = serializer.validated_data.get('username')

    
            return Response({'message': f'User with username [{username}] logged in.', 'token': serializer.validated_data.get('token')}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid data. Please provide valid data for login.'}, status=status.HTTP_400_BAD_REQUEST)



class DriverDetail(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes=[]

    def get(self, request, format=None):
        driver = Driver.objects.get(name=request.user)
        serializer = DriverSerializer(driver)
        return Response(serializer.data)

    def patch(self, request, format=None):
        try:
            driver = Driver.objects.get(name=request.user)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.data:
            serializer = DriverPatchSerializer(driver, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = DriverPatchSerializer(driver)
            return Response(serializer.data)


class DriverDelete(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = []

    def delete(self, request, format=None):
        try:
            driver = Driver.objects.get(name=request.user)
            user = User.objects.get(username=request.user.username)
            driver.delete()
            user.delete()
            return Response({'message': 'Driver deleted successfully.'}, status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PassengerDelete(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = []

    def delete(self, request, format=None):
        try:
            passenger = Passenger.objects.get(user=request.user)
            user = User.objects.get(username=request.user.username)
            passenger.delete()
            user.delete()
            return Response({'message': 'Passenger  deleted successfully.'}, status=status.HTTP_200_OK)
        except Passenger.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



