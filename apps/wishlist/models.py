# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login.models import User
import re

prod_regex = re.compile(r'[a-zA-Z0-9]+')

class ProductManager(models.Manager):
    def getUserList(self, id):
        return Product.objects.filter(wishes__id=id)
    def getOthersList(self, id):
        return Product.objects.exclude(wishes__id=id)
    def addItem(self, postData, id):
        errors = []
        if not prod_regex.match(postData['item']) or postData['item']=="":
            errors.append("Invalid product name")
        if len(postData['item']) < 3:
            errors.append("Product name is too short")
        try:
            prod = Product.objects.get(name=postData['item'])
            errors.append("A product with that name already exists")
        except: #product does not yet exist - OK
            pass
        message_to_views = {}
        if errors:
            message_to_views['status'] = False
            message_to_views['info'] = errors
        else:
            message_to_views['status'] = True
            user = User.objects.get(id=id)
            newProd = Product.objects.create(name=postData['item'], added_by=user)
            user.wished_for.add(newProd)
            message_to_views['info'] = newProd
        return message_to_views
    def addToList(self, data):
        user = User.objects.get(id=data['user_id'])
        product = Product.objects.get(id=data['product_id'])
        user.wished_for.add(product)
    def removeFromList(self, data):
        user = User.objects.get(id=data['user_id'])
        product = Product.objects.get(id=data['product_id'])
        user.wished_for.remove(product)
    def destroy(self, data):
        user = User.objects.get(id=data['user_id'])
        product = Product.objects.get(id=data['product_id'])
        if product.added_by != user:
            return "You do not have permission to delete this product"
        else:
            product.delete()

class Product(models.Model):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User)
    wishes = models.ManyToManyField(User, related_name="wished_for")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager()
