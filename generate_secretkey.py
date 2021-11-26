from django.core.management.utils import get_random_secret_key

with open('ancestry_web/secret_key.txt', 'w+') as f:
	f.write(get_random_secret_key())
