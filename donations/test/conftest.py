import datetime

import pytest
import random

from django.contrib.auth import get_user_model
from ..models import Institution, Donation, ContactForm, Category

User = get_user_model()


@pytest.fixture
def create_users():
	for i in range(5):
		User.objects.create(
			password="1234",
			first_name="User",
			last_name=f"{i + 1}",
			email=f"email{i + 1}@gmail.com"
		)


@pytest.fixture
def create_admin():
	return 	User.objects.create(
		password="1234",
		first_name="Admin",
		last_name=f"Superuser",
		email=f"admin@gmail.com",
		is_admin=True,
		is_superuser=True
	)


@pytest.fixture
def create_institutions_categories_donation():
	for i in range(5):
		User.objects.create(
			password="1234",
			first_name="User",
			last_name=f"{i + 1}",
			email=f"email{i + 1}@gmail.com"
		)
	for i in range(5):
		Category.objects.create(
			name=f"Category {i}"
		)
	institution = ['FOUNDATION', 'NON-GOVERNMENTAL', 'LOCAL COLLECTION']
	for i in institution:
		for j in range(5):
			c = Category.objects.first()
			institution = Institution.objects.create(
				name=f"Name {i} {j}",
				description=f"Description {j}",
				type=i,
			)
			institution.categories.add(c)
	institution = Institution.objects.first()
	user = User.objects.first()
	for i in range(5):
		Donation.objects.create(
			quantity=random.randint(1, 100),
			address="ul.Example 2",
			phone_number=999999999,
			city='Warsaw',
			zip_code=random.randint(1, 100),
			pick_up_date=datetime.date(1999, 11, 30),
			pick_up_time=datetime.time(8,0,0),
			pick_up_comment="Comment",
			institution=institution,
			user=user
		)


