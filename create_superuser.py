import os
from django.core.management import call_command
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    call_command('createsuperuser',
        username='admin',
        email=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'juan.villamoros@juzto.co'),
        password=os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'tiempo90'),
        interactive=False,
        verbosity=0)
