#12/20/2011 Author: Nick Moloney
from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from upload.models import Customer, Merchant, Product, Purchase

class UploadFileForm(forms.Form):
	file = forms.FileField()
	
def saveUploadedData(f):
	lineNum = 0
	grossRevenue = 0
	for line in f:
		if lineNum != 0:
			#split the line into an array of strings, separating on tabs
			items = line.split('\t')
			#get customer objects with the same name, if one exists
			customers = Customer.objects.filter(name__exact=items[0])
			c = None
			#if a customer exists with the same name, use that, otherwise create a new one
			#and save it to the database
			if len(customers) == 0:
				c = Customer(name=items[0])
				c.save()
			else:
				c = customers[0]
			
			#get/create Merchant and save to database
			merchants = Merchant.objects.filter(name=items[5], address=items[4])
			m = None
			if len(merchants) == 0:
				m = Merchant(name=items[5], address=items[4])
				m.save()
			else:
				m = merchants[0]
			
			#get/create product and save to database
			productPrice = float(items[2])
			products = Product.objects.filter(description=items[1], price=productPrice, merchant=m)
			p = None
			if len(products) == 0:
				p = Product(description=items[1], price=productPrice, merchant=m)
				p.save()
			else:
				p = products[0]
			
			#Create a new purchase in the database. since we could have multiple purchases with the same data values, 
			#there is no need to check the table for duplicates
			purchaseCount = int(items[3])
			purchase = Purchase(customer=c, product=p, count=purchaseCount)
			purchase.save()
			grossRevenue = grossRevenue + purchaseCount * productPrice #keep track of gross revenue as we go
		lineNum = lineNum + 1
	return grossRevenue
	
def upload(request):
	#if the page is posting data, retreive that data and add it to teh database, otherwise
	#return the form to upload data
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			revenue = saveUploadedData(request.FILES['file'])
			return HttpResponse("Your file has been uploaded with Gross Revenue of $" + str(revenue))
	else:
		form = UploadFileForm()
	return render_to_response('upload.html', {'form': form},
								context_instance=RequestContext(request))
