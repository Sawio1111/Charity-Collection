from django.core.management.base import BaseCommand

from donations.models import Category, Institution, Donation
from .commands_utils import create_institution, create_4_categories, create_4_user, create_donation


class Command(BaseCommand):
	help = 'Insert Institutions, Categories, Donations to database'

	def handle(self, *args, **options):
		create_4_categories()

		for i in range(4):
			create_institution()

		create_4_user()

		for i in range(10):
			create_donation()

