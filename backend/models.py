from operator import mod, truediv
from turtle import mode, ondrag
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.
class User(AbstractUser):
    
    def __str__(self):
        return self.username

"""
class BoxManager(models.Manager):
    def create(self, **kwargs):
        length = kwargs['length']
        breadth = kwargs['breadth']
        height = kwargs['height']
        kwargs['volume'] = length * breadth * height
        kwargs['area'] = 2 * (length * breadth + length * height + breadth * height)
        return super().create(**kwargs)

    def update(self, *args, **kwargs):
        pass
"""

class Box(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="creator_of", editable=False)
    length = models.FloatField(null=False, blank=False, default=1, validators=[MinValueValidator(1)])
    breadth = models.FloatField(null=False, blank=False, default=1, validators=[MinValueValidator(1)])
    height = models.FloatField(null=False, blank=False, default=1, validators=[MinValueValidator(1)])
    volume = models.FloatField(null=False, blank=False, default=1, validators=[MinValueValidator(1)])
    area = models.FloatField(null=False, blank=False, default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    #objects = BoxManager()

    class Meta:
        ordering = ['length', 'breadth', 'height', 'area', 'volume']

    def __str__(self):
        return f"volume {self.volume} cuboid by {self.created_by.username} at {self.created_at}"

    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        length = self.length
        breadth = self.breadth
        height = self.height
        if 'length' in kwargs:
            length = kwargs['length']
        if 'breadh' in kwargs:
            length = kwargs['breadh']
        if 'height' in kwargs:
            length = kwargs['height']
        volume = length * breadth * height
        area = 2 * (length * breadth + length * height + breadth * height)
        box = Box.objects.get(pk=kwargs['id'])
        box.volume = volume
        box.area = area
        return box.save()
    """