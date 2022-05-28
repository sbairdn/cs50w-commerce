from django.contrib.auth.models import AbstractUser
from django.db import models
from requests import request

MAX_PRICE_DIGITS = 6  # Max price is $9,999.99

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True, related_name="watchlister")
    bids = models.ManyToManyField('Bid', blank=True, related_name="bidder")


class Category(models.TextChoices):
    ART = 'Art'
    ELECTRONICS = 'Electronics'
    FASHION = 'Fashion'
    HOME = 'Home'
    TOYS = 'Toys'


class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=1000)
    start_price = models.DecimalField(max_digits=MAX_PRICE_DIGITS, decimal_places=2, null=True)
    current_price = models.DecimalField(max_digits=MAX_PRICE_DIGITS, decimal_places=2, null=True)
    image = models.ImageField(upload_to="images", blank=True)
    category = models.CharField(choices=Category.choices, max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postings", null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        string = ""
        string += "Active" if self.is_active else "Inactive"
        return f" listing: '{self.title}' by {self.poster} for ${self.start_price} at {self.datetime}"

class Bid(models.Model):
    price = models.DecimalField(max_digits=MAX_PRICE_DIGITS, decimal_places=2, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

class Comment(models.Model):
    text = models.CharField(max_length=500)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="comments")
    datetime = models.DateTimeField(auto_now_add=True, null=True)

