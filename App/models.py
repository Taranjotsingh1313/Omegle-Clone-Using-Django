from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Waiting(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    

class Connected(models.Model):
    user_1 = models.OneToOneField(User,on_delete=models.CASCADE)
    user_2 = models.OneToOneField(User,related_name="user2",on_delete=models.CASCADE)

class GroupModel(models.Model):
    group = models.CharField(max_length=255)
    users = models.ManyToManyField(User)