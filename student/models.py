from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group


# Create your models here.

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user', verbose_name='User')
    date_of_birth = models.DateField(null=True, blank=True, db_column='date_of_birth', verbose_name='Date of Birth')
    address = models.CharField(max_length=255, null=True, blank=True, db_column='address', verbose_name='Address')
    city_town = models.CharField(max_length=150, null=True, blank=True, db_column='city_town', verbose_name='City/Town')
    country = models.CharField(max_length=150, null=True, blank=True, db_column='country', verbose_name='Country')
    photo = models.ImageField(upload_to='photos/', null=True, blank=True, verbose_name='Profile Picture')

    def __repr__(self):
        return self.user.username


    def __str__(self):
        return self.user.username
    
    class Meta:
        db_table = 'Student'
        ordering = ['-id']


@receiver(post_save, sender=Student)  # Use your custom user model if applicable
def assign_group_to_user(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='Student')  # Replace 'YourGroupName' with the actual group name
        instance.user.groups.add(group)