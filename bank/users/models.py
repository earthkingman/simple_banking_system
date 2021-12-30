from django.db import models

# Create your models here.
class User(models.Model):
    email =  models.CharField(max_length=50)
    password =  models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)