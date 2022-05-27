from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlist_users")


class Category(models.TextChoices):
    ART = 'Art'
    ELECTRONICS = 'Electronics'
    FASHION = 'Fashion'
    HOME = 'Home'
    TOYS = 'Toys'


class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(choices=Category.choices, max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postings")
    def __str__(self):
        string = ""
        string += "Active" if self.is_active else "Inactive"
        return f" listing: '{self.title}' by {self.poster} for ${self.starting_bid}"

class Bid(models.Model):
    pass

class Comment(models.Model):
    text = models.CharField(max_length=500)

