from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):

	def create_user(self, email, password, **kwargs):
		if not email:
			raise ValueError('The email have to be set')
		user = self.model(email=self.normalize_email(email), **kwargs)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password):
		user = self.create_user(
			email,
			password=password,
		)
		user.is_superuser = True
		user.is_admin = True
		user.save(using=self._db)
		return user


class User(AbstractUser):
	username = None
	email = models.EmailField(verbose_name='email address', unique=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin


