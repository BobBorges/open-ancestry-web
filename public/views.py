from django.shortcuts import render
from ancestry_web.instance_details import this_instance
from django.contrib.auth.models import User
from private.models import Person, Source, AlternativeName

def landing_page(request):
	context = {}
	context.update(this_instance)
	return render(request, 'public/landing-page.html', context)

def statistics(request):
	surnames = {}
	ppl_objs = Person.objects.all()
	an_objs = AlternativeName.objects.all()

	for person in ppl_objs:
		if person.surname_at_birth not in surnames:
			surnames[person.surname_at_birth] = 1
		else:
			surnames[person.surname_at_birth] += 1

	for an in an_objs:
		if len(an.alternate_surname) > 0:
			if an.alternate_surname not in surnames:
				surnames[an.alternate_surname] = 1
			else:
				surnames[an.alternate_surname] += 1			

	surnames = {k: v for k, v in sorted(surnames.items(), key=lambda item: item[1], reverse=True) if v > 2}

	context= {}
	context['surnames'] = surnames
	context['num_users'] = len(User.objects.all())
	context['num_people'] = len(ppl_objs)
	context['num_sources'] = len(Source.objects.all())
	return render(request, 'public/stats.html', context)

def about(request):
	context = {}
	return render(request, 'public/about.html', context)