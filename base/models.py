from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    
    # Use email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Language(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    code = models.TextField(blank=False)
    # Takes a snapshot everytime we save
    updated = models.DateTimeField(auto_now=True)
    # Takes a snapshot only when created
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    # Takes a snapshot only when created
    created = models.DateTimeField(auto_now_add=True)

     # To view the newest Message first
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body



class Explain(models.Model):
    explain = models.TextField(max_length=4000)

    def __str__(self):
        return self.explain


class Translate(models.Model):
    first_language = models.CharField(max_length=200, null=True)
    second_language = models.CharField(max_length=200, null=True)
    translate = models.TextField(max_length=4000)


    def __str__(self):
        return self.translate