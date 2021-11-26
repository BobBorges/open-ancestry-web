from django.contrib import admin
from .models import *




class UIPAdmin(admin.ModelAdmin):
	fields = ['user', 'person']
	list_display = ['user', 'person']



admin.site.register(UserIsPerson, UIPAdmin)