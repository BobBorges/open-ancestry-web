from ancestry_web.instance_details import this_instance
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserIsPersonForm
from .models import UserIsPerson

@login_required
def I_am_Person(request):
	context = {}

	try:
		currentuser = UserIsPerson.objects.get(user=request.user)
		return redirect('person-details', principle_id=currentuser.id)
	except:
		if request.method == 'POST':
			userispersonform = UserIsPersonForm(request.POST)
			context['userispersonform'] = userispersonform
			if userispersonform.is_valid():
				newUIP = UserIsPerson.objects.create(
					user = request.user,
					person = userispersonform.cleaned_data['person']
				)
				newUIP.save()
				return redirect('person-details', principle_id=newUIP.person.id)
		else:
			userispersonform = UserIsPersonForm()
			context['userispersonform'] = userispersonform

	return render(request, 'authentication/user-is-person.html', context)


def register_view(request):
	context = {}
	context.update(this_instance)
	return render(request, 'authentication/register.html', context)