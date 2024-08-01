# tasks/management/commands/initialize_categories.py
from django.core.management.base import BaseCommand
from tryapp.models import Category

class Command(BaseCommand):
    help = 'Create a default category if it does not exist'

    def handle(self, *args, **kwargs):
        Category.objects.get_or_create(name='General')
        self.stdout.write(self.style.SUCCESS('Successfully initialized categories'))
