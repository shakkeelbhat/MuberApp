from django.urls import path
from muberapp.views import PassengerRegister, PassengerLogin, PassengerDetail, DriverList, ChangeDriverLike,DriverRegister, DriverLogin, DriverDetail,HomeView, PassengerDelete, DriverDelete

urlpatterns = [

    path('', HomeView.as_view()),

    path('passengers/register/', PassengerRegister.as_view()),
    path('passengers/login/', PassengerLogin.as_view()),
    path('passengers/detail/', PassengerDetail.as_view()),#get and update his details
    path('passengers/drivers/', DriverList.as_view()),
    path('passengers/like/', ChangeDriverLike.as_view()),

    
    path('drivers/register/', DriverRegister.as_view()),
    path('drivers/login/', DriverLogin.as_view()),
    path('drivers/detail/', DriverDetail.as_view()),
    path('drivers/delete/', DriverDelete.as_view()),
    path('passengers/delete/', PassengerDelete.as_view()),
]

