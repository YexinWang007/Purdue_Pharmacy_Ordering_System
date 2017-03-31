from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length=1000,help_text="i.e. david")
    phone_number= models.IntegerField(help_text="i.e. 7651111111")
    contact_email= models.CharField(max_length=200,help_text="i.e. david@purdue.edu")
    #login = models.ForeignKey(Login, blank=True, null=True)
    def __str__(self):
        return self.client_name
    def __unicode__(self):
        return self.client_name

class Order(models.Model):
    def __str__(self):
        return '%09d' % self.pk

    def __unicode__(self):
        return '%09d' % self.pk

    def get_order_number(self):  # for future generating order number
        return '%09d' % self.pk

        # associates to one Client table line

    client_obj = models.ForeignKey(Client, blank=True, null=True)

    # order info
    # order_number = get_order_number()  # for future generating order number
    ORDER_STATUS_CHOICES = (
        ('new', 'Products Ordered'),
        ('filled', 'Order Filled'),
        ('remove', 'Taken Out of Inventory'),
        ('ready', 'Order Ready for Pick Up'),
        ('billing', 'Order Delivered'),
        ('complete', 'Billing Complete')
    )
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='new')
    comment = models.TextField(max_length=1000, default="If you have any comments, please add it here")
    date_time = models.DateTimeField(auto_now_add=True)

class Drug(models.Model):  # This is the Drug table for detailed drug info

    # class functions
    def __str__(self):
        return self.drug_brand + " - " + self.drug_name

    def __unicode__(self):
        return self.drug_brand + " - " + self.drug_name

    # associate to one Order table line
    order_obj = models.ForeignKey(Order, blank=True, null=True)

    # drug info
    drug_brand = models.CharField(max_length=200)
    drug_name = models.CharField(max_length=200)
    strength = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)

class Product_List(models.Model):
    product_brand = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_strength = models.CharField(max_length=50)
    price=models.CharField(max_length=50)


class Wish_List(models.Model):
    client_obj_wish = models.ForeignKey(Client, blank=True, null=True)
    wish_drug_name = models.CharField(max_length=200)
    wish_drug_brand = models.CharField(max_length=200)
    wish_drug_strength=models.CharField(max_length=50)
    wish_drug_price=models.CharField(max_length=50)

class Shopping_Cart(models.Model):
    client_obj_shopping = models.ForeignKey(Client)
    shopping_drug_brand = models.CharField(max_length=200)
    shopping_drug_name = models.CharField(max_length=200)
    shopping_strength = models.CharField(max_length=50)
    shopping_quantity = models.IntegerField(default=0)