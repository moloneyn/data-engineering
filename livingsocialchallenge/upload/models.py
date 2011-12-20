from django.db import models

# Create a customer, merchant, product and purchase model to each have
# a table in the database
class Customer(models.Model):
	name = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name
	
class Merchant(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=75)
	
	def __unicode__(self):
		return self.name + " " + self.address
	
class Product(models.Model):
	description = models.CharField(max_length=70)
	price = models.DecimalField(max_digits=15, decimal_places=2)
	merchant = models.ForeignKey(Merchant)
	
	def __unicode__(self):
		return self.description + " " + str(self.price) + " " + str(self.merchant)
	
class Purchase(models.Model):
	customer = models.ForeignKey(Customer)
	product = models.ForeignKey(Product)
	count = models.IntegerField()
	
	def __unicode__(self):
		return str(self.customer) + " " + str(self.product) + " " + str(self.count)
	
