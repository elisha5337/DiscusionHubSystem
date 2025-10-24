from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)  # Title of the post
    content = models.TextField()               # Content of the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)      # Timestamp of last update

    def __str__(self):
        return self.title  # Return the title when the object is printed


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)  # Link to the BlogPost
    author = models.CharField(max_length=100)                     # Name of the author
    content = models.TextField()                                   # Comment content
    created_at = models.DateTimeField(auto_now_add=True)          # Timestamp of creation

    def __str__(self):
        return f"{self.author}: {self.content[:20]}"  # Return a short snippet of the comment
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
         return self.name

class Room(models.Model):
    host =models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True)
    participants= models.ManyToManyField(
        User,related_name='participants',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at','-updated_at']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at','-updated_at']
    def __str__(self):
        return self.body[0:50]


