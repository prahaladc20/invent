from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _ # If you need optional


# Create your models here.

# class User(AbstractUser):
#     username = models.CharField(max_length=10, unique=True)
#     email = models.EmailField(_('email address'), unique=True)
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

#     def __str__(self):
#         return "{}".format(self.email)

class Inventory(models.Model):
	author 			=	models.ForeignKey(User, on_delete=models.CASCADE)
	product_id 		= 	models.AutoField(null=False,primary_key=True)
	product_name 	= 	models.CharField(max_length=200)
	vendor 			= 	models.CharField(max_length=200)
	mrp 			= 	models.FloatField(max_length=10)
	batch_num		= 	models.IntegerField()
	batch_date 		=	models.DateField()
	quantity 		= 	models.IntegerField()
	# status 			= 	models.IntegerField()

	def __str__(self):
		return self.product_name
	        
class InventoryApproval(models.Model):
	author 			=	models.ForeignKey(User, on_delete=models.CASCADE)
	product_id 		= 	models.AutoField(null=False,primary_key=True)
	product_name 	= 	models.CharField(max_length=200)
	vendor 			= 	models.CharField(max_length=200)
	mrp 			= 	models.FloatField(max_length=10)
	batch_num		= 	models.IntegerField()
	master_id		= 	models.IntegerField(null=True)
	batch_date 		=	models.DateField()
	quantity 		= 	models.IntegerField()
	action 			= 	models.CharField(max_length=20,null=True)
	status 			= 	models.CharField(max_length=20)

	def __str__(self):
		return self.product_name