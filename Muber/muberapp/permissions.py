from rest_framework import permissions
from .models import Passenger




class IsPremiumPassenger(permissions.BasePermission):
    message = 'Adding likes is restricted to premium passengers.'

    def has_permission(self, request, view):
        passenger = Passenger.objects.get(user=request.user)
        return passenger.total_rides > 3
