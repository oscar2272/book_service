from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.sites import AlreadyRegistered

try:
    admin.site.register(User)
except AlreadyRegistered:
    pass