from django.db import models
from startup.models import Startup
import datetime
	
class Rent(models.Model):
	month = models.CharField(max_length= 100 , null=True)
	startup = models.ForeignKey(Startup,on_delete=models.CASCADE,null=True)
	room_no = models.CharField(max_length= 100 , null=True)
	paid = models.CharField(max_length= 100 , null=True)
	curr = models.BooleanField(default=False)
	duration = models.CharField(max_length= 100 , null=True)
	date_alloted = models.DateField(default=datetime.date.today)
	
# class Mentor(models.Model):
# 	user = models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
# 	name = models.CharField( max_length= 100 , null=True)
# 	email = models.CharField( max_length= 100 , null=True)
# 	phone_number = models.CharField( max_length= 100 , null=True)
# 	startups = models.ManyToManyField("startup.Startup",blank=True,null=True)
# 	description = models.CharField( max_length= 10000 , null=True)
# 	image = models.FileField(upload_to='profile_photos/',default='profile_photos/default.jpg')
# 	def __str__(self):
# 		return str(self.name)


