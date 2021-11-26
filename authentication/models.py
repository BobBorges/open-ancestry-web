from django.contrib.auth.models import User
from django.db import models
from private.models import Person

# Create your models here.
class UserIsPerson(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT, unique=True)
	person = models.ForeignKey(Person, on_delete=models.PROTECT, unique=True)

	def __str__(self):
		return f'User {self.user} is {self.person}'