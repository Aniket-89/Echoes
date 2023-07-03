from django.db import models
from django.urls import reverse
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# Create your models here.


class Author(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    biography   = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.user.username)

class Post(models.Model):
    author      = models.ForeignKey(Author, on_delete=models.CASCADE)
    title       = models.CharField(max_length=120)
    content     = HTMLField()
    summary     = models.TextField(null=True, blank=True)
    pub_date    = models.DateField(default=timezone.now)
    image       = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title
    
    # def get_absolute_url(self):
    #     return reverse('post', kwargs={'pk':self.id})