from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass
class Post(models.Model):
    username=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    user=models.ForeignKey(User,on_delete=models.CASCADE , related_name="creater")
    likes= models.ManyToManyField(User,related_name="likes" )
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            
        } 
    def __str__(self):
        return f"{self.user} to {self.content}"
class Profile(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE , related_name="follower",default=None)
    following=models.ForeignKey(User,on_delete=models.CASCADE , related_name="following",default=None)