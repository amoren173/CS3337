from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MainMenu(models.Model):
    item = models.CharField(max_length=200,unique=True)
    link = models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.item

class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0)
    ratingscount = models.IntegerField(default=0)
    overallrating = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


# CartItem model for shopping cart functionality
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.book.price  # Calculate total price based on quantity

    def __str__(self):
        return f"{self.book.name} (x{self.quantity})"