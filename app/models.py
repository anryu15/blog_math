from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, related_name="subcategories" ,on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=255)
    content = models.TextField("本文")
    created = models.DateTimeField("作成日", default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    img = models.ImageField(blank=True, null=True, upload_to = 'media/')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to = 'media/')
    goodcomment = models.ManyToManyField(User, related_name='good', blank=True)
    badcomment = models.ManyToManyField(User, related_name='bad', blank=True)

class AccountUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numgood = models.IntegerField('good',default=0)
    contents = models.TextField("contents", null=True) 

    def __str__(self):
        return self.user.username