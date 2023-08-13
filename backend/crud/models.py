from django.db import models

from tag.models import Tag
from user.models import User
from django.urls import reverse
# from taggit.managers import TaggableManager
# Create your models here.

"""
class Tag(models.Model): #
    tag_content = models.TextField(unique=True) #
    tag_filename = models.CharField(null=True, blank=True, default="", max_length=500) #
"""
class Product(models.Model):
    product_code = models.AutoField(primary_key=True)
    product_name = models.CharField(null=False, max_length=100)
    user =  models.ForeignKey('user.User', related_name='user_id', on_delete=models.CASCADE)
    # price = models.IntegerField(default=0)
    description = models.TextField(null=False)
    filename = models.CharField(null=True, blank=True, default="", max_length=500)
    images = models.ImageField(blank=True, null=True, upload_to='images/')
    modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)
    # tagImage = models.ManyToManyField(TagImage, verbose_name = "태그 이미지")
    tag = models.ManyToManyField(Tag, verbose_name = "태그")

    def __str__(self):
        return self.product_name

class Clothes(models.Model):
    myJson = models.CharField(null=True, blank=True, default="", max_length=500)

