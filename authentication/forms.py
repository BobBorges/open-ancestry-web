from django import forms
from django.forms import ModelForm
from private.models import Person
from .models import UserIsPerson

class UserIsPersonForm(forms.ModelForm):

	class Meta:
		model = UserIsPerson
		fields = ['person']