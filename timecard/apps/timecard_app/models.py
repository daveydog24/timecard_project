from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import bcrypt
import pytz

class UserManager(models.Manager):
    # validating the user and their information
    def validate_user(self, postData):
        errors = {} 

        if len(postData['first_name']) < 4:
            errors['first_name'] = "Name can not be less than 3 characters."

        if len(postData['last_name']) < 4:
            errors['last_name'] = "Username can not be less than 3 characters."

        if len(postData['email']) < 1:
            errors['email'] = "Email cant be less than 1 character."

        if len(postData['password']) < 8:
            errors['password'] = "password cant be less than 8 characters."

        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "passwords do not match please reconfirm."
            
        try:
            validate_email(postData['email'])
        except ValidationError:
            errors['email'] = "This is not a valid email."
        else:
            if User.objects.filter(email=postData['email']):
                errors['email'] = "This email is already registered to an account, sorry."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    date_joined = models.DateTimeField()
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=1) # 1 = admin, 2 = manager, 3 = employee
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Points(models.Model):
    amount = models.CharField(max_length=255)
    user = models.OneToOneField(User, related_name="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Report(models.Model):
    achievement = models.TextField()
    challenge = models.TextField()
    improvement = models.TextField()
    recipient = models.ManyToManyField(User, related_name="recipients")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

