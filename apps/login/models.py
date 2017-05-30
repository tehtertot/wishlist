# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import date
import bcrypt

class UserManager(models.Manager):
    def addUser(self, postData):
        #validations
        errors = []
        if len(postData['name']) < 3:
            errors.append("Name should be at least 3 characters long")
        try:
            User.objects.get(username=postData['username'])
            errors.append("This username is already in use. Try again.")
        except:
            if len(postData['username']) < 3:
                errors.append("Username should be at least 3 characters long")
        if len(postData['password']) < 8:
            errors.append("Password is too short")
        if postData['password'] == "":
            errors.append("Password is required")
        if postData['password'] != postData['confirm']:
            errors.append("Passwords do not match")
        if postData['hired'] == "":
            errors.append("No hired date specified")
        if postData['hired'] > str(date.today()):
            errors.append("Hire date must be in the past")

        messages_to_views = {}
        if errors:
            messages_to_views['status'] = False
            messages_to_views['info'] = errors
        else:
            messages_to_views['status'] = True
            hashedpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            messages_to_views['info'] = User.objects.create(name=postData['name'], username=postData['username'], password=hashedpw, date_hired=postData['hired'])
        return messages_to_views
    def signUserIn(request, postData):
        errors = []
        try:
            user = User.objects.get(username=postData['username'])
            if bcrypt.hashpw(postData['password'].encode(), user.password.encode()) != user.password.encode():
                errors.append("Wrong password. Try again.")
        except:
            errors.append("No user registered with that username")
        messages_to_views = {}
        if errors:
            messages_to_views['status'] = False
            messages_to_views['info'] = errors
        else:
            messages_to_views['status'] = True
            messages_to_views['info'] = user
        return messages_to_views

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    date_hired = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
