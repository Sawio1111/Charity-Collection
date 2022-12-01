import pytest


from django.test import Client
from django.contrib.auth import get_user_model
from ..models import Institution, Donation, Category

User = get_user_model()


@pytest.mark.django_db
def test_index_display(client, create_institutions_categories_donation):
	response = client.get('/')
	bags = Donation.objects.count()
	organisations = Donation.objects.values('institution_id').distinct().count()
	foundations = Institution.objects.filter(type="FOUNDATION").count()
	assert response.status_code == 200
	assert response.context['bags'] == bags
	assert response.context['organisation'] == organisations
	assert len(response.context['foundations']) == foundations


@pytest.mark.django_db
def test_categories_display(create_institutions_categories_donation):
	categories = Category.objects.count()
	user = User.objects.first()
	c = Client()
	c.force_login(user=user)
	response = c.get('/donation/')
	assert response.status_code == 200
	assert len(response.context['categories']) == categories


@pytest.mark.django_db
def test_login_page(client):
	response = client.get('/login/')
	assert response.status_code == 200


@pytest.mark.django_db
def test_register(client):
	user = {
		'first_name': 'Name',
		'last_name': 'Surname',
		'email': 'Email@gmail.com',
		'password1': '1234qwert',
		'password2': '1234qwert'
	}
	response = client.post('/register/', user)
	user_database = User.objects.first()
	assert user_database.first_name == 'Name'
	assert response.status_code == 302


@pytest.mark.django_db
def test_profile(client, create_institutions_categories_donation):
	c = Client()
	user = User.objects.first()
	c.force_login(user=user)
	response = c.get('/profile/')
	assert response.status_code == 200
	assert response.context['user'] == user