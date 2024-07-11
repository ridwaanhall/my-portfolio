# base/management/commands/export_data.py
from django.core.management.base import BaseCommand
from django.core import serializers
from base.models import Project, Sidebar, Home, About, Logo, Education, Skill, Certificate, Credential, Message, Quote


class Command(BaseCommand):
    help = 'Export data from the database'

    def handle(self, *args, **kwargs):
        models = [
            Project, Sidebar, Home, About, Logo, Education, Skill, Certificate,
            Credential, Message, Quote
        ]
        for model in models:
            model_name = model.__name__.lower()
            data = serializers.serialize('json', model.objects.all())
            file_name = f'{model_name}_data.json'
            with open(file_name, 'w') as f:
                f.write(data)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully exported {model_name.capitalize()} data'))
