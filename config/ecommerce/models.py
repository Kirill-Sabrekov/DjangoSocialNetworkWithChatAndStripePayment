from django.db import models
from users.models import CustomUser
from network.models import Posts

class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Posts, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    count_buy = models.IntegerField(default=1)
    paid = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    
