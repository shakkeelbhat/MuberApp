from django.db import models
from django.contrib.auth.models import User

class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="passengers")
    total_rides = models.IntegerField(default=0)
    age = models.IntegerField()

class Driver(models.Model):
    LANGUAGES = [
        ('EN', 'English'),
        ('UR', 'Urdu'),
        ('HI', 'Hindi'),
        ('OT', 'Others'),
    ]

    name = models.OneToOneField(User, on_delete=models.CASCADE,related_name="drivers")
    positive_likes = models.IntegerField(default=0)
    negative_likes = models.IntegerField(default=0)
    car_model = models.CharField(max_length=255)
    age = models.IntegerField()
    languages = models.CharField(max_length=2, choices=LANGUAGES, default='EN')
