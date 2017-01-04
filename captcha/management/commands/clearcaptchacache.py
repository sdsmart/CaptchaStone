# clearcaptchacache.py
from django.core.management.base import BaseCommand
from captcha.models import Captcha


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Deleting all captchas from cache.')
        try:
            Captcha.objects.all().delete()
        except Exception as e:
            print(e)
        print('Successfully deleted all captchas from cache.')
