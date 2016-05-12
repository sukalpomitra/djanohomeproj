from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):
	use_in_migrations = True
	def create_user(self, facebook_id, first_name, last_name, email, access_token, password=None):
		email = self.normalize_email(email)
		user = self.model(facebook_id=facebook_id, first_name=first_name,last_name=last_name,email=email,access_token=access_token)
		user.set_password(password)
		user.save(using=self._db)
		return user
		
		def create_superuser(self, username, email, password, **extra_fields):
			extra_fields.setdefault('is_staff', True)
			extra_fields.setdefault('is_superuser', True)

class User(AbstractBaseUser):
	objects = UserManager()
	facebook_id = models.IntegerField(unique=True)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=150)
	access_token = models.CharField(max_length=20)
	USERNAME_FIELD = 'facebook_id'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'access_token']
	class Meta:
		db_table = "users"

class Photo(models.Model):
	#user_id = models.IntegerField
	image = models.ImageField(_('image'), blank=True, null=True, upload_to='item_images/')
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
		related_name='uploaded_item_images',blank=False,)
	class Meta:
		db_table = "user_photos"