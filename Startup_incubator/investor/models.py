from django.db import models

import startup
from login.models import Type
import datetime
from django.contrib.auth.models import User

class Investor(models.Model):
	
	user = models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
	name = models.CharField( max_length= 100 , null=True)
	email = models.CharField( max_length= 100 , null=True)
	phone_number = models.CharField( max_length= 100 , null=True,default="Not added")
	expertise = models.CharField(max_length=1000,null=True,default="Not added")
	startups = models.ManyToManyField("startup.Startup",blank=True,null=True)
	description = models.CharField( max_length= 10000 , null=True,default="Not added")
	investment_range = models.CharField(max_length=190,null=True,default="Not added")
	image = models.FileField(upload_to='profile_photos/',default='profile_photos/default.jpg')
	def __str__(self):
		return str(self.name)

class Connections(models.Model):
	sentfrom = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="sent_from")
	sentto = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="sent_to")
	date = models.DateField(default=datetime.date.today)
	response = models.BooleanField(default=False)
	accept = models.BooleanField(default=False)