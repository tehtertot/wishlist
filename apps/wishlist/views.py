# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, User

def index(request):
    context = { 'user_wishlist': Product.objects.getUserList(request.session['user_id']),
                'other_items': Product.objects.getOthersList(request.session['user_id']) }
    return render(request, 'wishlist/index.html', context)

def addItem(request):
    if request.method == "GET":
        return render(request, 'wishlist/addItem.html')
    elif request.method == "POST":
        fromModel = Product.objects.addItem(request.POST, request.session['user_id'])
        if fromModel['status']:
            return redirect('wishlist:index')
        else:
            for error in fromModel['info']:
                messages.add_message(request, messages.ERROR, error)
            return redirect('wishlist:addItem')

def show(request, id):
    if request.method == "GET":
        context = { 'product': Product.objects.get(id=id) }
        return render(request, 'wishlist/show.html', context)

def addToList(request, id):
    data = { 'user_id': request.session['user_id'],
             'product_id': id }
    Product.objects.addToList(data)
    return redirect('wishlist:index')

def remove(request, id):
    data = { 'user_id': request.session['user_id'],
             'product_id': id }
    Product.objects.removeFromList(data)
    return redirect('wishlist:index')

def destroy(request, id):
    data = { 'user_id': request.session['user_id'],
             'product_id': id }
    if Product.objects.destroy(data):
        context = {'message': Product.objects.destroy(data)}
        return render(request, 'wishlist/deny.html', context)
    return redirect('wishlist:index')
