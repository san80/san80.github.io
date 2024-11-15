from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Category(models.Model):
    name=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"


class auction_list(models.Model):
    title=models.CharField(max_length=64)
    description=models.TextField()
    image_url=models.URLField(blank=True ,null=True)
    starting_bid=models.DecimalField(max_digits=10, decimal_places=2)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='auctions', blank=True, null=True)
    is_active=models.BooleanField(default=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    timestamp=models.DateTimeField(auto_now_add=True)
    winner=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='winner')

    def __str__(self):
        return f"{self.title}"


User.add_to_class('watchlist', models.ManyToManyField(auction_list, blank=True, related_name='watched_by'))


    

class bids(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    list_item=models.ForeignKey(auction_list, on_delete=models.CASCADE, related_name="bids")
    price=models.DecimalField(max_digits=10, decimal_places=2)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bid {self.price} on {self.list_item.title}"
    
    

class comments(models.Model):
    person=models.ForeignKey(User,on_delete=models.CASCADE, related_name="comments")
    item=models.ForeignKey(auction_list, on_delete=models.CASCADE, related_name="comments")
    comment=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.person.username} on {self.item.title}"
    
