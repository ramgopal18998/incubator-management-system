from django.db import models

from django.contrib.auth.models import User

# Create your

STATUS_CHOICES = (
    ('startup', 'startup'),
    ('investor', 'investor'),
    ('mentor', 'mentor'),
    )

class Type(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	typ = models.CharField(choices=STATUS_CHOICES,max_length=100,null=False,default="startup")

	def __str__(self):
		return str(self.user.username + " (" + str(self.typ) + ")")




