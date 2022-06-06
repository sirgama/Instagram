from django.contrib import admin
from .models import Tag, Post, FollowersCount, Comments

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(FollowersCount)
admin.site.register(Comments)