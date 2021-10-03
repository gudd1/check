from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



class User(AbstractUser):
      CandidateName = models.CharField(max_length=50,unique=False)




