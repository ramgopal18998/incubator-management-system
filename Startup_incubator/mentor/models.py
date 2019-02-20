from django.db import models
from login.models import Type
import startup

class Mentor(models.Model):
	user = models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
	name = models.CharField( max_length= 100 , null=True)
	email = models.CharField( max_length= 100 , null=True)
	phone_number = models.CharField( max_length= 100 , null=True)
	experience = models.CharField( max_length= 100 , null=True)
	expertise = models.CharField( max_length= 100 , null=True)
	description = models.CharField( max_length= 10000 , null=True)
	image = models.FileField(upload_to='profile_photos/',default='profile_photos/default.jpg')
	def __str__(self):
		return str(self.name)




