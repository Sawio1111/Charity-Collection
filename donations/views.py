import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView, LogoutView, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .models import Donation, Category, Institution
from .forms import RegistrationForms, UpgradeAuthenticationForm, DonationForm

User = get_user_model()


class LandingPageView(View):
	template_name = 'donations/index.html'

	def get(self, request, *args, **kwargs):
		number_bags = Donation.objects.all().count()
		number_organisation = Donation.objects.values('institution_id').distinct().count()
		foundation = Institution.objects.filter(type='FOUNDATION')
		non_governmental = Institution.objects.filter(type='NON-GOVERNMENTAL ORGANISATION')
		local_collection = Institution.objects.filter(type='LOCAL COLLECTION')
		context = {
			'bags': number_bags,
			'organisation': number_organisation,
			'foundations': foundation,
			'non_governmental': non_governmental,
			'local_collections': local_collection,
		}
		return render(request, template_name=self.template_name, context=context)


class AddDonationView(LoginRequiredMixin, View):
	template_name = 'donations/form.html'

	def get(self, request, *args, **kwargs):
		categories = Category.objects.all()
		context = {
			'categories': categories,
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


class UserProfileView(LoginRequiredMixin, ListView):
	template_name = 'donations/profil.html'

	def get_queryset(self):
		return Donation.objects.filter(user_id=self.request.user.id)

	def get(self, request, *args, **kwargs):
		return super().get(self, request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user'] = User.objects.get(id=self.request.user.id)
		return context


class FormResponseView(LoginRequiredMixin, View):
	template_name = 'donations/form-confirmation.html'

	def get(self, request, *args, **kwargs):
		return render(request, template_name=self.template_name, context={'info': kwargs['info']})


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


class ApiFormRequest(LoginRequiredMixin, View):
	form_class = DonationForm

	def post(self, request, *args, **kwargs):
		form = json.loads(request.body)['form']
		print(form)
		form['user'] = self.request.user
		form_class = self.form_class(form)
		if form_class.is_valid():
			form_class.save()
			return JsonResponse({'response': 'Data saved'})
		return JsonResponse({'response': 'Wrong data'})


class ApiFoundation(LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		list_foundation = Institution.objects.filter(type="FOUNDATION").values('name', 'description')
		paginator = Paginator(list_foundation, 2)
		page_number = kwargs['page']
		page_obj = paginator.get_page(page_number)
		return JsonResponse({'pages': page_obj.number, 'obj': list(page_obj.object_list)})
