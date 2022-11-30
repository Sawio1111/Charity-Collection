from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import ValidationError

from .models import Donation

User = get_user_model()


class RegistrationForms(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].widget.attrs['placeholder'] = 'Email'
		self.fields['first_name'].required = True
		self.fields['first_name'].widget.attrs['placeholder'] = 'Imie'
		self.fields['last_name'].required = True
		self.fields['last_name'].widget.attrs['placeholder'] = 'Nazwisko'

	password1 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
		required=True,
	)
	password2 = forms.CharField(
		widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}),
		required=True,
	)

	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
		]

	def clean(self):
		form = super().clean()
		password1 = form.get('password1')
		password2 = form.get('password2')
		name = form.get('first_name')
		surname = form.get('last_name')

		if password1 != password2:
			raise ValidationError("Hasła nie są takie same")

		if len(password1) < 8:
			raise ValidationError('Hasło powinno mieć przynajmniej 8 znaków')

		if len(name) < 3 or len(surname) < 3:
			raise ValidationError('Nie prawidłowe imie lub nazwisko')


class UpgradeAuthenticationForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'Email'
		self.fields['password'].widget.attrs['placeholder'] = 'Hasło'


class DonationForm(forms.ModelForm):
	class Meta:
		model = Donation
		fields = '__all__'
		exclude = ['is_taken']
