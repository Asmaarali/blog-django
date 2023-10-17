from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name=models.CharField(null=True, max_length=50)
    email=models.EmailField(null=True, max_length=254,unique=True)
    bio=models.TextField(null=True)
    image=models.ImageField(null=True,default="avatar.svg")
    USERNAME_FIELD = 'email'   #login with email (You've specified the USERNAME_FIELD as 'email'. This means that users will log in using their email address instead of the default username.)
    REQUIRED_FIELDS = []        #(You've set REQUIRED_FIELDS to an empty list, indicating that no additional fields are required when creating a user. This is typically used when you don't require any extra fields during user registration.)

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    participants=models.ManyToManyField(User, related_name='participants',blank=True) 
    created=models.DateTimeField(auto_now_add=True) #not change only once create
    updated=models.DateTimeField(auto_now=True) #changable

    class Meta:
        ordering=['-updated','-created']
    def __str__(self):
        return self.name

class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True) #not change only once create
    updated=models.DateTimeField(auto_now=True) #changable

    def __str__(self):
        return self.body[0:50]
    