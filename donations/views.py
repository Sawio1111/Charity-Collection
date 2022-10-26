import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Donation, Category, Institution
from .forms import RegistrationForms, UpgradeAuthenticationForm


class LandingPageView(View):
	template_name = 'donations/index.html'

	def get(self, request, *args, **kwargs):
		number_bags = Donation.objects.all().count()
		number_organisation = Donation.objects.values('institution_id').distinct().count()
		context = {
			'bags': number_bags,
			'organisation': number_organisation,
			'index': 'index',
		}
		return render(request, template_name=self.template_name, context=context)


class AddDonationView(LoginRequiredMixin, View):
	template_name = 'donations/form.html'

	def get(self, request, *args, **kwargs):
		categories = Category.objects.all()
		institutions = Institution.objects.all()
		context = {
			'categories': categories,
			'institutions': institutions
		}
		return render(request, template_name=self.template_name, context=context)


class LoginToView(LoginView):
	template_name = 'donations/login.html'
	form_class = UpgradeAuthenticationForm

	def form_invalid(self, form):
		return redirect(reverse_lazy('register') + '#register')

	def get_success_url(self):
		return reverse_lazy('main')


class LogoutToView(LogoutView):
	pass


class RegisterView(CreateView):
	template_name = 'donations/register.html'
	form_class = RegistrationForms

	def form_valid(self, form):
		response = super().form_valid(form)
		cd = form.cleaned_data
		self.object.set_password(cd['password1'])
		self.object.save()
		return response

	def get_success_url(self):
		return reverse_lazy('login') + '#login'


class ApiCategories(LoginRequiredMixin, View):

	def post(self, request, *args, **kwargs):
		list_id = json.loads(request.body)['categories_id']
		institution = [list(Institution.objects.filter(categories=id)) for id in list_id]
		response = []
		all_institution = Institution.objects.all()
		for all_ins in all_institution:
			hit = 0
			for ins in institution:
				if all_ins in ins:
					hit += 1
				if hit == len(list_id):
					response.append({
						'name': all_ins.name,
						'description': all_ins.description,
						'type': all_ins.get_type_display(),
						'id': all_ins.id
					})
		return JsonResponse({'response': response})
