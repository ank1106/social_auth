from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Creates superuser'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # create superuser
        user, created = User.objects.get_or_create(username="dunzo")
        user.is_staff = True
        user.is_superuser = True
        user.set_password('dunzoadmin')
        user.save()
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.name = "Dunzo"
        profile.email = "dunzo@dunzo.com"
        profile.phone_number = "9090909090"
        profile.save()
        self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
        
