from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#customer user model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('farmer', 'Farmer'),
        ('expert', 'Expert'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username
    
#  farmer profile model

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    crop_types = models.CharField(max_length=255)
    land_size = models.FloatField()
    preferred_language = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


# query module

class Query(models.Model):
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('assigned', 'Assigned'),
        ('review', 'In Review'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    )

    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    crop = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# query media

class QueryMedia(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='queries/')


# expert response

class ExpertResponse(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    response_text = models.TextField(blank=True, null=True)
    audio_response = models.FileField(upload_to='responses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


# knowledge base


class Category(models.Model):
    name = models.CharField(max_length=100)

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    crop = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


# notifications

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


# market prices

class MarketPrice(models.Model):
    crop = models.CharField(max_length=100)
    mandi = models.CharField(max_length=100)
    price = models.FloatField()
    date = models.DateField()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    crop = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


