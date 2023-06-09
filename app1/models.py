from django.db import models
from django.core import validators
# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    adress=models.TextField()
    profile_pic=models.ImageField(upload_to='sab')

    def __str__(self):
        return self.adress