from django.db import models
from django.db.models.fields.files import ImageField
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import os

from app_users.models import News


# Create your models here.
class Standard(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def save_subject_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.id:
        filename = 'Subject_Pictures/{}.{}'.format(instance.id, ext)
    return os.path.join(upload_to, filename)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name='subjects')
    image = models.ImageField(upload_to=save_subject_image, blank=True, verbose_name='Subject Image')
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def save_lesson_files(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.id:
        filename = 'lesson_files/{}/{}.{}'.format(instance.id, instance.id, ext)
        if os.path.exists(filename):
            new_name = str(instance.id) + str('1')
            filename = 'lesson_images/{}/{}.{}'.format(instance.id, new_name, ext)
    return os.path.join(upload_to, filename)


class Lesson(models.Model):
    Standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=250)
    position = models.PositiveSmallIntegerField(verbose_name="Chapter no.")
    slug = models.SlugField(null=True, blank=True)
    video = models.FileField(upload_to=save_lesson_files, verbose_name="Video", blank=True, null=True)
    ppt = models.FileField(upload_to=save_lesson_files, verbose_name="Presentations", blank=True)
    Notes = models.FileField(upload_to=save_lesson_files, verbose_name="Notes", blank=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('curriculum:lesson_detail', kwargs={'standard': self.Standard.slug, 'subject': self.subject.slug, 'slug': self.name})


class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE, related_name='comments_lesson')
    new_name = models.ForeignKey(News, null=True, blank=True, on_delete=models.CASCADE, related_name='comments_new')
    comm_name = models.CharField(max_length=100, blank=True)
    # reply = models.ForeignKey("Comment", null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    field = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name

    class Meta:
        ordering = ['-date_added']


class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    field = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)


def save_course_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.title:
        filename = 'CoursePicture/{}.{}'.format(instance.title, ext)
    return os.path.join(upload_to, filename)


class Courses(models.Model):
    title = models.CharField(max_length=100, blank=True, unique=True)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to=save_course_image, blank=True, verbose_name='Course Image')
    
    def __str__(self):
        return self.title