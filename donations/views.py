from django.shortcuts import render
from django.views import View
# Create your views here.


class LandingPageView(View):
	template_name = 'donations/index.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


class AddDonationView(View):
	template_name = 'donations/form.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


class LoginView(View):
	template_name = 'donations/login.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)


class RegisterView(View):
	template_name = 'donations/register.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name)

