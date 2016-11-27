from django.db import models

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length=1000,default="i.e. david")
    phone_number= models.IntegerField(default="i.e. 7651111111")
    contact_email= models.CharField(max_length=200,default="i.e. david@purdue.edu")
    #login = models.ForeignKey(Login, blank=True, null=True)
    def __str__(self):
        return self.client_name
    def __unicode__(self):
        return self.client_name

class Order(models.Model):
    drug_name = models.CharField(max_length=1000, default="i.e. Amoxicillin")
    drug_brand = models.CharField(max_length=1000, default="i.e. Decodron")
    quantity = models.IntegerField(default=0)
    strength = models.CharField(max_length=1000, default="i.e. 500ml")
    ready_to_pickup = models.BooleanField(default=False)
    already_pickup = models.BooleanField(default=False)
    doctor_name = models.CharField(max_length=1000, default="i.e. Paul1027")
    doctor_email = models.CharField(max_length=1000, default="i.e. Paul1027@purdue.edu")
    client_obj= models.ForeignKey(Client, blank=True, null=True)
    comment = models.TextField(max_length=1000, default="Any additional information")
    def __str__(self):
        return self.drug_name

    def __unicode__(self):
        return self.drug_name

