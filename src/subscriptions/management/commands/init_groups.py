import helpers
from typing import Any
from django.core.management.base import BaseCommand
from subscriptions.models import PERMISSIONS
from django.contrib.auth.models import Group

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        for permission, _ in PERMISSIONS:
            group_name = f'{permission.capitalize()} Users'
            if not Group.objects.filter(name=group_name).exists():
                print(group_name, 'Dont Exists')
                pass
            else:
                print(group_name, 'Exists')
                pass
            # Group(name=group_name).save()
