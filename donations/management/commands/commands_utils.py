import faker
import random
import datetime

from django.contrib.auth.views import get_user_model

from donations.models import Institution, Donation, Category

faker = faker.Faker("pl-PL")

User = get_user_model()


def create_4_categories():
	categories = ['Zabawki', 'Ubrania', 'Jedzenie', 'Inne']
	for category in categories:
		Category.objects.create(
			name=category
		)


def create_institution():
	institution = Institution.objects.create(
		name=faker.company(),
		description=faker.sentence(),
		type=random.choice(Institution.institution_type)[1],
	)
	category = list(Category.objects.all())
	institution.categories.add(random.choice(category))


def create_4_user():
	data = {
		'John': {'email': 'John@gmail.com', 'password': 'John'},
		'Steve': {'email': 'Steve@gmail.com', 'password': 'Steve'},
		'Alice': {'email': 'Alice@gmail.com', 'password': 'Alice'},
		'Young': {'email': 'Young@gmail.com', 'password': 'Young'},
			}
	for value in data.values():
		user = User.objects.create(
			last_name=faker.last_name(),
			first_name=value['password'],
			email=value['email'],
		)
		user.set_password(value['password'])
		user.save()


def create_donation():
	institutions = Institution.objects.all()
	users = User.objects.all()
	return Donation.objects.create(
		quantity=random.randint(1, 9),
		address=faker.address(),
		phone_number=faker.msisdn(),
		city=faker.city(),
		zip_code=faker.postcode(),
		pick_up_date=datetime.datetime.today() + datetime.timedelta(days=random.randint(1, 30)),
		pick_up_time=datetime.time(8,0,0),
		pick_up_comment=faker.sentence(),
		institution_id=random.choice(institutions).id,
		user_id=random.choice(users).id,
	)
