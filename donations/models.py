from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class MyUserManager(BaseUserManager):

	def create_user(self, email, password, **kwargs):
		if not email:
			raise ValueError('The email have to be set')
		user = self.model(email=self.normalize_email(email), **kwargs)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password, **kwargs):
		kwargs.setdefault('is_admin', True)
		kwargs.setdefault('is_superuser', True)

		return self.create_user(email, password, **kwargs)


class User(AbstractUser):
	username = None
	email = models.EmailField(verbose_name='email address', unique=True)
	is_admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = MyUserManager()

	def __str__(self):
		return self.email

	@property
	def is_staff(self):
		return self.is_admin


class Category(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "category"
		verbose_name_plural = "categories"


class Institution(models.Model):
	institution_type= (
		('FOUNDATION', 'Fundacja'),
		('NON-GOVERNMENTAL ORGANISATION', 'Organizacja pozarządowa'),
		('LOCAL COLLECTION', 'Zbiórka lokalna'),
	)
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=256)
	type = models.CharField(choices=institution_type, default='FOUNDATION', max_length=64)
	categories = models.ManyToManyField(Category, related_name='categories')
	display = models.BooleanField(default=True)

	def __str__(self):
		return self.name


class Donation(models.Model):
	status = (
		('TAKEN', 'zabrany'),
		('NOT TAKEN', 'do odbioru'),
	)

	quantity = models.PositiveBigIntegerField()
	categories = models.ManyToManyField(Category, related_name='donation_categories')
	institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=256)
	phone_number = models.PositiveBigIntegerField()
	city = models.CharField(max_length=64)
	zip_code = models.CharField(max_length=6)
	pick_up_date = models.DateField()
	pick_up_time = models.TimeField()
	pick_up_comment = models.CharField(max_length=1024)
	user = models.ForeignKey(User, null=True, default=None, on_delete=models.SET_NULL)
	is_taken = models.CharField(choices=status, default='NOT TAKEN', max_length=64)


class ContactForm(models.Model):
	name = models.CharField(max_length=64)
	surname = models.CharField(max_length=64)
	message = models.CharField(max_length=64)
	data_send = models.DateTimeField(auto_now_add=True)
