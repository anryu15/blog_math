from django.contrib import admin
from .models import Post, AccountUser, Category, SubCategory, Comment

admin.site.register(Post)
admin.site.register(AccountUser)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Comment)