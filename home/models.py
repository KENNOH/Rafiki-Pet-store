from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Pet_services
# Create your models here.


class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    owner = models.CharField(max_length=255,default="John Doe")
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    rating = models.IntegerField()
    pet_instance = models.ForeignKey(Pet_services, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
