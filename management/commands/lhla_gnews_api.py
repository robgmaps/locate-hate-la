from django.core.management.base import BaseCommand, CommandError
from lhla.views import *

class Command(BaseCommand):
	help = 'Check GNews API for new articles'

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		gnews_api()
		self.stdout.write(self.style.SUCCESS("finished!"))