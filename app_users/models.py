from django.db import models
from django.contrib.auth.models import User
import os
from django.db.models.fields import CharField, TextField
from django.db.models.fields.files import ImageField
from django.urls import reverse


def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)


class UserProfileInfo(models.Model):
    # creating a relationship with user class (not inheriting)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # adding additional attributes
    bio = models.CharField(max_length=500)
    profile_pic = models.ImageField(upload_to=path_and_rename, verbose_name="Profile Picture", blank=True)
    teacher = 'teacher'
    student = 'student'
    parent = 'parent'
    user_types = [
        (teacher, 'teacher'),
        (student, 'student'),
        (parent, 'parent'),
    ]
    user_type = models.CharField(max_length=10, choices=user_types, default=student)

    def __str__(self):
        return self.user.username

def path_and_rename_news(instance, filename):
    upload_to = 'Images/News/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.id:
        filename = '{}.{}'.format(instance.id, ext)
    return os.path.join(upload_to, filename)


class News(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=50, unique=True)
    body = models.TextField(max_length=500)
    news_pic = models.ImageField(upload_to=path_and_rename_news, verbose_name="Profile Picture", blank=True)

    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return self.title

def path_and_rename_teacher(instance, filename):
    upload_to = 'Images/HonoraryTeachers/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.id:
        filename = '{}.{}'.format(instance.id, ext)
    return os.path.join(upload_to, filename)


class HonoraryTeachers(models.Model):
    name = models.CharField(max_length=100, unique=True)
    about = TextField(max_length=500)
    science = CharField(max_length=100)
    image = ImageField(upload_to=path_and_rename_teacher, verbose_name="Profile Picture", blank=True)
    
    def __str__(self):
        return self.name
