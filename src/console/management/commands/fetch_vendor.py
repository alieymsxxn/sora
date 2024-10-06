import helpers
from typing import Any
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    VENDOR_STATICFILES = {
        # 'saas-theme.min.css': 'https://raw.githubusercontent.com/codingforentrepreneurs/SaaS-Foundations/main/src/staticfiles/theme/saas-theme.min.css',
        'flowbite.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css',
        'flowbite.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js',
        'flowbite.min.js.map': 'https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map'
    }
    STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')
    def handle(self, *args: Any, **options: Any):
        for filename, url in self.VENDOR_STATICFILES.items():
            destination = self.STATICFILES_VENDOR_DIR / filename
            status = helpers.download(url=url, out_path=destination, parent_mkdir=True)
            if status:
                self.stdout.write(self.style.SUCCESS(f'Successfully downloaded {filename} into {destination}'))
            else:
                self.stdout.write(self.style.ERROR(f'Successfully downloaded {filename} into {destination}'))