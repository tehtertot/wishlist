# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'login/index.html')

def login(request):
    if request.method == "GET":
        return redirect('login:index')
    if request.method == "POST":
        response_from_models = User.objects.signUserIn(request.POST)
        #if successful login
        if response_from_models['status']:
            setSessionVariables(request, response_from_models['info'])
            return redirect('wishlist:index')
        #unsuccessful login
        else:
            for error in response_from_models['info']:
                messages.add_message(request, messages.ERROR, error, extra_tags="login")
            return redirect('login:index')

def register(request):
    if request.method == "GET":
        return redirect('login:index')
    elif request.method == "POST":
        response_from_models = User.objects.addUser(request.POST)
        #successfully registered
        if response_from_models['status']:
            setSessionVariables(request, response_from_models['info'])
            return redirect('wishlist:index')
        #unsuccessfully registered
        else:
            for error in response_from_models['info']:
                messages.add_message(request, messages.ERROR, error, extra_tags="register")
            return redirect('login:index')

def logout(request):
    request.session.pop('username')
    request.session.pop('user_id')
    return redirect('login:index')

def setSessionVariables(request, user):
    request.session['username'] = user.name
    request.session['user_id'] = user.id
