from django.db import models
from investor.models import Investor
from mentor.models import Mentor
from django.contrib.auth.models import User
from login.models import Type
from datetime import datetime

class Founder(models.Model):
	name = models.CharField( max_length= 100 , null=True)
	email = models.CharField( max_length= 100 , null=True)
	phone_number = models.CharField( max_length= 100 , null=True)
	address = models.CharField( max_length= 100 , null=True)
	def __str__(self):
		return str(self.name)

class Startup(models.Model):
	user = models.ForeignKey(Type,on_delete=models.CASCADE)
	name  = models.CharField( max_length= 100 , null=True)
	founder = models.OneToOneField(Founder,blank=True,null=True)
	investors = models.ManyToManyField(Investor,blank=True)
	mentors = models.ManyToManyField(Mentor,blank=True)
	address = models.CharField( max_length= 100 , null=True)
	phone_number = models.CharField( max_length= 100 , null=True)
	email = models.CharField( max_length= 100 , null=True)
	description = models.CharField( max_length= 10000 , null=True)
	dipp = models.BooleanField(default=False)
	image = models.FileField(upload_to='profile_photos/',default='profile_photos/default.jpg')
	dippno = models.CharField(max_length=100,blank=True,null=True)
	cat = models.CharField(max_length=100,blank=True,null=True)
	experience = models.CharField(max_length=100,null=True,default=3)
	turnover = models.CharField(max_length=100,null=True,default=10)
	no_of_employees = models.CharField(max_length=100,null=True,default=100)
	admin_funded = models.BooleanField(default=False)

	#recommended_investors = models.ManyToManyField(Investor,blank=True)
	def __str__(self):
		return str(self.name)

class Tickets(models.Model):
	title = models.CharField(max_length=100,null=True)
	startup = models.ForeignKey(Startup,on_delete=models.CASCADE)
	issue = models.CharField(max_length=1000,null=True)
	status = models.BooleanField(default=False)
	solved_date = models.DateTimeField(null=True,blank=True)
	issue_date = models.DateTimeField(auto_now=True, auto_now_add=False)



class Bookings(models.Model):
	startup = models.ForeignKey(Startup,on_delete=models.CASCADE,null=True	)
	date = models.DateField(null=True,blank=True)
	day = models.CharField(max_length=100,null=True,blank=True)
	time = models.IntegerField(null=True,blank=True)
	status = models.BooleanField(default=False)
# class Connection_investor(models.Model):
# 	startup = models.ForeignKey(Startup,on_delete=models.CASCADE,null=True)
# 	investor = models.ForeignKey(Investor,on_delete=models.CASCADE,null=True)
# 	S_to_I = models.BooleanField(default=True)
# 	accepted = models.BooleanField(default=False)
# 	pending = models.BooleanField(default=True)

# class Connection_mentor(models.Model):
# 	startup = models.ForeignKey(Startup,on_delete=models.CASCADE,null=True)
# 	mentor = models.ForeignKey(Mentor,on_delete=models.CASCADE,null=True)
# 	S_to_M = models.BooleanField(default=True)
# 	accepted = models.BooleanField(default=False)
# 	pending = models.BooleanField(default=True)

	
# class Incubation_request(models.Model):
# 	startup = models.ForeignKey(Startup,on_delete=models.CASCADE)
# 	ppt = models.FileField(null=True,upload_to='Incubation_ppts/')
# 	pending = models.BooleanField(default=True)
# 	accepted = models.BooleanField(default=False)
# 	date_applied = models.DateTimeField(auto_now=True, auto_now_add=False)

TASK_STATUS = ( ('Pending','Pending'),('In Progress','In Progress') )
class Tasks(models.Model):
	startup = models.ForeignKey(Startup,on_delete=models.CASCADE)
	status = models.CharField(max_length=500, blank=False, null=False, default='Pending', choices=TASK_STATUS)
	date_assigned = models.DateTimeField(auto_now=True, auto_now_add=False)


# image = models.ImageField(upload_to='category/', default="/media/category/default.png")