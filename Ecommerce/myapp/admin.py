from django.contrib import admin
from .models import BlogPost,Comment,Post,Message,Topic,Room
# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Topic)
admin.site.register(Room)
