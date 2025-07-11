from django.db import models
from core.models import AbstractModel
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
import random
from django.template.defaultfilters import slugify



# Create your models here.


class Product(AbstractModel):
    CATEGORY = (
        ('FOR KIDS', 'FOR KIDS'),
        ('FOR ANIMAL', 'FOR ANIMAL'),
    )
    title = models.CharField(max_length=500 , null=False, blank=False)
    color = models.ManyToManyField('Color', blank=True)
    grid = models.ManyToManyField('Grid',  blank=True)
    category = models.CharField(max_length=50, null=False, blank=False, choices=CATEGORY)
    description = models.TextField(null=False, blank=False)
    detail = models.CharField(max_length=55, null=False, blank=False)
    image = models.ImageField(upload_to='ProductIMGs/', null=False, blank=False)
    in_stock = models.BooleanField(default=True)
    price = models.BigIntegerField(null=False, blank=False)
    slug = models.SlugField(max_length=500, null=False, unique=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
       self.slug = slugify(self.title)
       super(Product, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return self.slug

   
    

class Color(AbstractModel):
    title=models.CharField(max_length=50)
   
    def __str__(self):
        return self.title
   

class Grid(AbstractModel):
    title=models.CharField(max_length=50)

    def __str__(self):
        return self.title
    
  

    
