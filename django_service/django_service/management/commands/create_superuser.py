# # yourappname/management/commands/create_superuser.py
#
# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import Group
# from bonds.models import Users
#
#
# class Command(BaseCommand):
#     help = 'Create a superuser with specific permissions'
#
#     def handle(self, *args, **kwargs):
#         username = 'admin'
#         password = 'admin'
#
#         if not Users.objects.filter(name=username).exists():
#             user = Users.objects.create_superuser(
#                 name=username,
#                 password=password,
#                 is_staff=True,
#                 is_superuser=True
#             )
#             group = Group.objects.get(name='DeviceViewers')
#             user.groups.add(group)
#             self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
#         else:
#             self.stdout.write(self.style.WARNING('Superuser already exists'))
