from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.forms import ModelForm
from django.shortcuts import render, redirect
from functools import reduce
from .forms import ReplyForm, ResearchForm, PersonEditForm, CreatePersonForm, CreateSourceForm, SourceEditForm, EventEditFormA, EventEditFormB, CreateEventForm, CreateEpochForm, EditEpochForm, CreateNuggetForm, EditNuggetForm, CreateRelationshipForm, EditRelationshipForm, CreateAlternativeNameForm, EditAlternativeNameForm
from .models import Person, Event, AlternativeName, Relationship, Epoch, BiographicalInfoNugget, Research, ResearchReply, Source
import os


@login_required
def people_landing(request):
	people = Person.objects.all().order_by('surname_at_birth', 'given_name')
	context = {
		'people': people 
	}
	return render(request, 'private/people-welcome.html', context)



@login_required
def person_details(request, principle_id):
	# birth event
	try:
		be = Event.objects.get(event_people=principle_id, event_type='birth')
	except:
		be = None
	# death event
	try:
		de = Event.objects.get(event_people=principle_id, event_type='death')
	except:
		de = None
	# Alternative names
	try:
		ANs = AlternativeName.objects.filter(principle=principle_id)
	except:
		ANs = None
	#################
	# RELATIONSHIPS #
	#################
	# parents
	try:
		parents_raw = Relationship.objects.filter(principle=principle_id, relationship_type="child of")
		parents = {}
		for p in parents_raw:
			try:
				pbe = Event.objects.get(event_people=p.referent.id, event_type='birth')
			except:
				pbe = None
			pde = None
			if not Person.objects.get(id=p.referent_id).living:
				living = False
				try:
					pde = Event.objects.get(event_people=p.referent.id, event_type='death')
				except:
					pde = None
			else:
				living = True
			parents[p] = {
				'birth': pbe, 
				'death': pde,
				'living': living
			}
	except:
		parents = None


	# guardians
	try:
		guardians_raw = Relationship.objects.filter(principle=principle_id, relationship_type="ward of")
		guardians = {}
		for p in guardians_raw:
			try:
				pbe = Event.objects.get(event_people=p.referent.id, event_type='birth')
			except:
				pbe = None
			pde = None
			if not Person.objects.get(id=p.referent_id).living:
				living = False
				try:
					pde = Event.objects.get(event_people=p.referent.id, event_type='death')
				except:
					pde = None
			else:
				living = True
			guardians[p] = {
				'birth': pbe, 
				'death': pde,
				'living': living
			}
	except:
		guardians = None


	# siblings
	if parents_raw:
		siblings = {}
		half_siblings = {}
		for raw_p in parents_raw:
			children_of_parent = Relationship.objects.filter(principle=raw_p.referent_id, relationship_type='parent of').exclude(referent=principle_id)
			for child_o_p in children_of_parent:
				try:
					child_o_pbe = Event.objects.get(event_people=child_o_p.referent_id, event_type='birth')
				except:
					child_o_pbe = None

				child_o_pde = None
				if not Person.objects.get(id=child_o_p.referent_id).living:
					living = False
					try:
						child_o_pde = Event.objects.get(event_people=sp.referent_id, event_type='death')
					except:
						child_o_pde = None
				else:
					living = True

				ps_o_c = Relationship.objects.filter(principle=child_o_p.referent_id, relationship_type='child of')
				
				if len(ps_o_c) < 2:
					sib_bool = True
					coparent = None
					if child_o_p.referent not in half_siblings:
						half_siblings[child_o_p.referent] = {
							'id': child_o_p.referent_id,
							'birth': child_o_pbe,
							'living': living,
							'death': child_o_pde,
							'coparent':	coparent
						}
				else:
					for p_o_c in ps_o_c:
						if p_o_c.referent != raw_p.referent:
							sib_bool = False
							coparent = None
							for pr in parents_raw:
								if pr.referent == p_o_c.referent:
									sib_bool = True
								else:
								#	print("FFFFF")
									coparent = p_o_c
								
							if sib_bool:
								if child_o_p.referent not in siblings:
									siblings[child_o_p.referent] = {
										'id': child_o_p.referent_id,
										'birth': child_o_pbe,
										'living': living,
										'death': child_o_pde
									}
							else:
							#	print(coparent)
								if child_o_p.referent not in half_siblings:
									half_siblings[child_o_p.referent] = {
										'id': child_o_p.referent_id,
										'birth': child_o_pbe,
										'living': living,
										'death': child_o_pde,
										'coparent':	coparent
									}
		if len(siblings) == 0:
			siblings = None
		#print(half_siblings)
		if len(half_siblings) == 0:
			half_siblings = None
	else:
		siblings = None
		half_siblings = None

	# spouses
	try:
		spouses_raw = Relationship.objects.filter(principle=principle_id, relationship_type='spouse of')
		spouses = {}
		for sp in spouses_raw:
			try:
				spbe = Event.objects.get(event_people=sp.referent_id, event_type='birth')
			except:
				spbe = None
			spde = None

			if not Person.objects.get(id=sp.referent_id).living:
				living = False
				try:
					spde = Event.objects.get(event_people=sp.referent_id, event_type='death')
				except:
					spde = None
			else:
				living = True

			try:
				sp_m_epoch = Epoch.objects.filter(epoch_people=sp.referent_id, epoch_type='marriage')
				pr_m_epoch = Epoch.objects.filter(epoch_people=principle_id, epoch_type='marriage')
				m_epochs = [] 
				for e in pr_m_epoch:
					if e in sp_m_epoch:
						m_epochs.append(e)
			except:
				m_epoch = None
			spouses[sp] = {
				'birth': spbe,
				'death': spde,
				'living': living,
				'marriages': m_epochs
			}
	except:
		spouses = None

	# children
	try:
		children_raw = Relationship.objects.filter(principle=principle_id, relationship_type='parent of') 
		if len(children_raw) == 0:
			children = None
		else:
			children = {}
			for child in children_raw:
				try:
					cbe = Event.objects.get(event_people=child.referent_id, event_type='birth')
				except:
					cbe = None
				cde = None
				if not Person.objects.get(id=child.referent_id).living:
					living = False
					try:
						cde = Event.objects.get(event_people=child.referent_id, event_type='death')
					except:
						cde = None
				else:
					living = True
				try:
					child_parents = Relationship.objects.filter(principle=child.referent_id, relationship_type='child of')
					coparent = None
					for child_parent in child_parents:
						if principle_id != child_parent.referent_id:
							coparent = Person.objects.get(id=child_parent.referent_id)
						else:
							pass
				except:
					coparent = None

				children[child] = {
					'birth':cbe,
					'death':cde,
					'living': living,
					'coparent': coparent
				}
	except:
		children = None

	# wards

	try:
		wards_raw = Relationship.objects.filter(principle=principle_id, relationship_type='guardian of') 
		if len(wards_raw) == 0:
			wards = None
		else:
			wards = {}
			for child in wards_raw:
				try:
					cbe = Event.objects.get(event_people=child.referent_id, event_type='birth')
				except:
					cbe = None
				cde = None
				if not Person.objects.get(id=child.referent_id).living:
					living = False
					try:
						cde = Event.objects.get(event_people=child.referent_id, event_type='death')
					except:
						cde = None
				else:
					living = True

				wards[child] = {
					'birth':cbe,
					'death':cde,
					'living': living,	
				}
	except:
		wards = None

	#####################
	# Other life Events #
	#####################
	try:
		events = Event.objects.filter(event_people=principle_id).exclude(event_type='birth').exclude(event_type='death').order_by('event_date')
	except:
		events = None
	##########
	# Epochs #
	##########
	try:
		epochs = Epoch.objects.filter(epoch_people=principle_id).order_by('start_date')
	except:
		epochs = None
	##################
	# BioInfoNuggets #
	##################
	try:
		BINs = BiographicalInfoNugget.objects.filter(people=principle_id).order_by('start_date')
	except:
		BINs = None
	############
	# RESEARCH #
	############
	try:
		RQs = Research.objects.filter(principle=principle_id, item_type='question').order_by('created')
		research_questions = {}
		
		for RQ in RQs:
			RQR = ResearchReply.objects.filter(reply_to=RQ)
			if len(RQR) > 0:
				research_questions[RQ] = RQR
			else:
				 research_questions[RQ] = None
	except:
	#	print("FFFF")
		research_questions = None

	try:
		RTs = Research.objects.filter(principle=principle_id, item_type='theory')
		theories = {}
		for RT in RTs:
			RTR = ResearchReply.objects.filter(reply_to=RT)
			if len(RQR) > 0:
				theories[RT] = RTR
			else:
				 theories[RT] = None
	except:
		theories = None

	try:
		DEs = Research.objects.filter(principle=principle_id, item_type='dead end')
		dead_ends = {}
		for DE in DEs:
			DER = ResearchReply.objects.filter(reply_to=DE)
			if len(DER) > 0:
				dead_ends[DE] = DER
			else:
				 dead_ends[DE] = None
	except:
		dead_ends = None

	principle_obj = Person.objects.get(id=principle_id)
	context = {
		'people': Person.objects.all().order_by('surname_at_birth', 'given_name'),
		'principle': principle_obj,
		'birth_event': be,
		'death_event': de,
		'parents': parents,
		'guardians': guardians,
		'spouses': spouses,
		'children': children,
		'wards': wards,
		'siblings': siblings,
		'half_siblings': half_siblings,
		'events': events,
		'alternate_names': ANs,
		'epochs': epochs,
		'BINs': BINs,
		'research_questions': research_questions,
		'theories': theories,
		'dead_ends': dead_ends,
	}

	if request.method == 'POST':
	#	print(request.POST)
		if 'replyf' in request.POST:
			replyform = ReplyForm(request.POST)
			context['replyform'] = replyform
			if replyform.is_valid():
				robj = ResearchReply.objects.create(
					reply_to=Research.objects.get(id=request.POST['OP']),
					created_by=request.user,
					content=replyform.cleaned_data['content']
				)
				robj.save()
				return redirect('person-details', principle_id=principle_id)
		elif 'researchf' in request.POST:
			researchform = ResearchForm(request.POST)
			context['researchform'] = researchform
			if researchform.is_valid():
				resobj = Research.objects.create(
					title=researchform.cleaned_data['title'],
					item_type=researchform.cleaned_data['item_type'],
					content=researchform.cleaned_data['content'],
					research_is_private=researchform.cleaned_data['research_is_private'],
					principle=Person.objects.get(id=principle_id),
					created_by=request.user,
					active=True
				)
				resobj.save()
				return redirect('person-details', principle_id=principle_id)
		elif 'personeditf' in request.POST:
			personeditform = PersonEditForm(request.POST)
			context['personeditform'] = personeditform
			if personeditform.is_valid():
				persobj = Person.objects.get(id=principle_id)
				persobj.given_name = personeditform.cleaned_data['given_name']
				persobj.surname_at_birth = personeditform.cleaned_data['surname_at_birth']
				persobj.sex = personeditform.cleaned_data['sex']
				persobj.living = personeditform.cleaned_data['living']
				persobj.headshot = personeditform.cleaned_data['headshot']
				persobj.sources.set(personeditform.cleaned_data['sources'])
				persobj.save()
				return redirect('person-details', principle_id=principle_id)
		elif 'editalternatenamef' in request.POST:
			editalternativenameform = EditAlternativeNameForm(request.POST)
			context['editalternativenameform'] = editalternativenameform
			if editalternativenameform.is_valid():
				ANobj = AlternativeName.objects.get(id=editalternativenameform.cleaned_data['ANIDfield'])
				ANobj.alternate_first = editalternativenameform.cleaned_data['alternate_first']
				ANobj.alternate_surname = editalternativenameform.cleaned_data['alternate_surname']
				ANobj.alternative_type = editalternativenameform.cleaned_data['alternative_type']				
				ANobj.explanation = editalternativenameform.cleaned_data['explanation']
				ANobj.start_date_of_alternative = editalternativenameform.cleaned_data['start_date_of_alternative']
				ANobj.start_date_approximate = editalternativenameform.cleaned_data['start_date_approximate']
				ANobj.end_date_of_alternative = editalternativenameform.cleaned_data['end_date_of_alternative']
				ANobj.end_date_approximate = editalternativenameform.cleaned_data['end_date_approximate']
				ANobj.sources.set(editalternativenameform.cleaned_data['sources'])
				ANobj.save()
				return redirect('person-details', principle_id=principle_id)
		elif 'createalternativenaemf' in request.POST:
			createalternativenameform = CreateAlternativeNameForm(request.POST)
			context['createalternativenameform'] = createalternativenameform
			if createalternativenameform.is_valid():
				ANobj = AlternativeName.objects.create(
					alternate_first = createalternativenameform.cleaned_data['alternate_first'],
					alternate_surname = createalternativenameform.cleaned_data['alternate_surname'],
					alternative_type = createalternativenameform.cleaned_data['alternative_type'],			
					explanation = createalternativenameform.cleaned_data['explanation'],
					start_date_of_alternative = createalternativenameform.cleaned_data['start_date_of_alternative'],
					start_date_approximate = createalternativenameform.cleaned_data['start_date_approximate'],
					end_date_of_alternative = createalternativenameform.cleaned_data['end_date_of_alternative'],
					end_date_approximate = createalternativenameform.cleaned_data['end_date_approximate'],
					created_by = request.user,
					principle = principle_obj
				)
				ANobj.sources.set(createalternativenameform.cleaned_data['sources'])
				ANobj.save()
				return redirect('person-details', principle_id=principle_id)
	else:
		personeditform = PersonEditForm(instance=Person.objects.get(id=principle_id))
		context['personeditform'] = personeditform
		replyform = ReplyForm()
		context['replyform'] = replyform 
		researchform = ResearchForm()
		context['researchform'] = researchform
		createalternativenameform = CreateAlternativeNameForm()
		context['createalternativenameform'] = createalternativenameform
		editalternativenameform = EditAlternativeNameForm()
		context['editalternativenameform'] = editalternativenameform

	return render(request, 'private/person-view.html', context)



@login_required
def person_add(request):
	context = {
	'people': Person.objects.all().order_by('surname_at_birth', 'given_name'),
	}
	if request.method == 'POST':
		createpersonform = CreatePersonForm(request.POST)
		context['createpersonform'] = createpersonform
		if createpersonform.is_valid():
			pobj = Person.objects.create(
				given_name = createpersonform.cleaned_data['given_name'],
				surname_at_birth = createpersonform.cleaned_data['surname_at_birth'],
				sex = createpersonform.cleaned_data['sex'],
				living = createpersonform.cleaned_data['living'],
				headshot = createpersonform.cleaned_data['headshot'],
				created_by_user=request.user,
			)
			pobj.sources.set(createpersonform.cleaned_data['sources'])
			pobj.save()
			pid = pobj.id
			return redirect('person-details', principle_id=pid)
	else:
		createpersonform = CreatePersonForm()
		context['createpersonform'] = createpersonform

	return render(request,'private/person-add.html', context)



@login_required
def sources_landing(request):
	sources = Source.objects.all().order_by('source_date_of_creation')
	context = {
		'sources': sources 
	}

	return render(request, 'private/sources-welcome.html', context)



@login_required
def source_add(request):
	sources = Source.objects.all().order_by('source_date_of_creation')
	context = {
		'sources': sources 
	}
	if request.method == 'POST':
		createsourceform = CreateSourceForm(request.POST, request.FILES)
		context['createsourceform'] = createsourceform
		if createsourceform.is_valid():
			sobj = createsourceform.save(commit=False)
			sobj.created_in_DB_by_user = request.user
			sobj.save()
			sid = sobj.id
			return redirect('source-details', source_id=sid)
		else:
			print("ERROR private/views.py:", createsourceform.errors)
	else:
		createsourceform = CreateSourceForm()
		context['createsourceform'] = createsourceform

	return render(request,'private/source-add.html', context)



@login_required
def source_details(request, source_id):
	sources = Source.objects.all().order_by('source_date_of_creation')
	context = {
		'sources': sources 
	}
	srcobj = Source.objects.get(id=source_id)
	context['trgtsrcobj'] = srcobj

	if request.method == 'POST':
	#	print(request.POST)
		sourceeditform = SourceEditForm(request.POST)
		context['sourceeditform'] = sourceeditform
		if sourceeditform.is_valid():
			esrcobj = Source.objects.get(id=source_id)
			esrcobj.source_title = sourceeditform.cleaned_data['source_title']
			esrcobj.source_type = sourceeditform.cleaned_data['source_type']
			esrcobj.source_creator = sourceeditform.cleaned_data['source_creator']
			esrcobj.source_date_of_creation = sourceeditform.cleaned_data['source_date_of_creation']
			esrcobj.source_DOC_approximate = sourceeditform.cleaned_data['source_DOC_approximate']
			esrcobj.source_description = sourceeditform.cleaned_data['source_description']
			esrcobj.source_bibliographic_reference = sourceeditform.cleaned_data['source_bibliographic_reference']
			esrcobj.src_is_private = sourceeditform.cleaned_data['src_is_private']
			esrcobj.save()
			esrcid = srcobj.id
			return redirect('source-details', source_id=esrcid)
	else:
		sourceeditform = SourceEditForm(instance=Source.objects.get(id=source_id))
		context['sourceeditform'] = sourceeditform

	return render(request, 'private/source-view.html', context)
	#response['Content-Type'] = ''
	#response['x-Sendfile'] = os.path.join(settings.MEDIA_PRIV, srcobj.source_file.name)
	#return response


@login_required
def events_landing(request):
	events = Event.objects.all().order_by('event_date')
	context = {
		'events': events 
	}

	return render(request, 'private/events-welcome.html', context)



@login_required
def event_add(request):
	events = Event.objects.all().order_by('event_date')
	context = {
		'events': events 
	}

	if request.method == 'POST':
		createeventform = CreateEventForm(request.POST)
		context['createeventform'] = createeventform
	#	print(request.POST)

		if createeventform.is_valid():
			if createeventform.cleaned_data['event_type'] == 'birth' and len(createeventform.cleaned_data['event_people']) > 1:
				messages.error(request, "You can only select ONE person for a birth event.")
			elif createeventform.cleaned_data['event_type'] == 'death' and len(createeventform.cleaned_data['event_people']) > 1:
				messages.error(request, "You can only select ONE person for a death event.")
			else:
				newE = Event.objects.create(
					event_title = createeventform.cleaned_data['event_title'],
					created_by = request.user,
					event_type = createeventform.cleaned_data['event_type'],
					event_description = createeventform.cleaned_data['event_description'],
					event_date = createeventform.cleaned_data['event_date'],
					event_date_approximate = createeventform.cleaned_data['event_date_approximate'],
					place = createeventform.cleaned_data['place'],
					event_is_private = createeventform.cleaned_data['event_is_private']
				)
				newE.event_people.set(createeventform.cleaned_data['event_people'])
				newE.sources.set(createeventform.cleaned_data['sources'])
				newE.save()
				newEp = newE.event_people.all()
				#print('newEp:', len(newEp), '::', newEp)
				if newE.event_type == 'death':
					for involvedprsn in newEp:
						prsn_epochs = Epoch.objects.filter(epoch_people__in=[involvedprsn])
					#	print(prsn_epochs) 
						for pe in prsn_epochs:
							if len(pe.end_date) == 0:
						#		print('~~~', pe, newE.event_date, newE.event_date_approximate)
								pe.end_date = newE.event_date
								pe.end_date_approximate = newE.event_date_approximate
								pe.save()
						prsn_rels = Relationship.objects.filter(Q(principle=involvedprsn, relationship_type='spouse of') | Q(referent=involvedprsn, relationship_type='spouse of'))
						#print(prsn_rels) 
						for pr in prsn_rels:
							if not pr.end_date:
							#	print('~~~', pr)
								pr.end_date = newE.event_date
								pr.end_date_approximate = newE.event_date_approximate
								pr.save()

				elif newE.event_type == 'marriage' and len(newEp) == 2: 
					od = {
						'robj1': None,
						'robj2': None
					}			
					for idx, invp in enumerate(newEp, start=1):
						for x in newEp:
							if invp != x:
								newR_is_private = False
								if newE.event_is_private:
									newR_is_private = True
								try: 
									rel = Relationship.objects.get(
										principle = invp, 
										relationship_type = 'spouse of',
										referent = x
									)
									if not rel.start_date:
										rel.start_date = newE.event_date
										rel.start_date_approximate = newE.event_date_approximate
									rel.sources.add(*[x.id for x in newE.sources])
									rel.save()
									od[f'robj{idx}'] = rel.biderrel
								except:
									newR = Relationship.objects.create(
										created_by = request.user,
										principle = invp,
										relationship_type = 'spouse of',
										referent = x,
										start_date = newE.event_date,
										start_date_approximate = newE.event_date_approximate,
										end_date_approximate = False,
										relationship_is_private = newE.event_is_private
									)
									newR.sources.set(newE.sources.all())
									newR.save()
									#print('>>>>>', f'robj+{idx}')
									od[f'robj{idx}'] = newR

					O1 = od['robj1']
					O2 = od['robj2']
					O1.bidirrel = O2
					O2.bidirrel = O1
					O1.save()
					O2.save()

					IDs = [x.id for x in newEp]
					#print('IDs', IDs)
					epochs = Epoch.objects.annotate(count=Count('epoch_people')).filter(count=len(IDs))
					#print('EPOCHS1', len(epochs), '::', epochs)
					epochs = reduce(lambda p, id: epochs.filter(epoch_people=id), IDs, epochs)
					#print('EPOCHS2', len(epochs), '::', epochs)
					epochs = epochs.filter(epoch_type='marriage')
					if 	len(epochs) > 0:
						for epoch in epochs:
					#		print(len(epochs), '>>>>>>', epoch)
							if epoch.epoch_type == 'marriage':
								if not epoch.start_date:
									epoch.start_date = newE.event_date
									epoch.start_date_approximate = newE.event_date_approximate
								epoch.epoch_people.add(*IDs)
								epoch.sources.add(*[x.id for x in newE.sources.all()])
								epoch.save()

					else:
					#	print("creating epoch")
						newPOCH_is_private = False
						if newE.event_is_private:
							newPOCH_is_private = True
						newPOCH = Epoch.objects.create(
							epoch_title = newE.event_title,
							created_by = request.user,
							epoch_type = newE.event_type,
							start_date = newE.event_date,
							start_date_approximate = newE.event_date_approximate,
							end_date_approximate = False,
							epoch_is_private = newPOCH_is_private
						)
						newPOCH.epoch_people.set(newE.event_people.all())
						newPOCH.sources.set(newE.sources.all())
						newPOCH.save()
					#	print("---> created")

				elif newE.event_type == 'divorce' and len(newEp) == 2:
					od = {
						'robj1': None,
						'robj2': None
					}					
					for idx, invp in enumerate(newEp, start=1):
						for x in newEp:
							if invp != x:
								newR_is_private = False
								if newE.event_is_private:
									newR_is_private = True
								try: 
									rel = Relationship.objects.get(
										principle = invp, 
										relationship_type = 'spouse of',
										referent = x
									)
									if not rel.start_date:
										rel.end_date = newE.event_date
										rel.end_date_approximate = newE.event_date_approximate
									rel.sources.add(*[x.id for x in newE.sources])
									rel.save()
									od[f'robj{idx}'] = rel.biderrel
								except:
									newR = Relationship.objects.create(
										created_by = request.user,
										principle = invp,
										relationship_type = 'spouse of',
										referent = x,
										end_date = newE.event_date,
										end_date_approximate = newE.event_date_approximate,
										start_date_approximate = False,
										relationship_is_private = newE.event_is_private
									)
									newR.sources.set(newE.sources.all())
									newR.save()
									od[f'robj{idx}'] = newR

					O1 = od['robj1']
					O2 = od['robj2']
					O1.bidirrel = O2
					O2.bidirrel = O1
					O1.save()
					O2.save()


					IDs = [x.id for x in newEp]
					#print('IDs', IDs)
					epochs = Epoch.objects.annotate(count=Count('epoch_people')).filter(count=len(IDs))
					#print('EPOCHS1', len(epochs), '::', epochs)
					epochs = reduce(lambda p, id: epochs.filter(epoch_people=id), IDs, epochs)
					#print('EPOCHS2', len(epochs), '::', epochs)
					epochs = epochs.filter(epoch_type='marriage')
					if len(epochs) > 0:
						for epoch in epochs:
						#	print(len(epochs), '>>>>>>', epoch)
							if epoch.epoch_type == 'divorce':
								if not epoch.start_date:
									epoch.end_date = newE.event_date
									epoch.end_date_approximate = newE.event_date_approximate
								epoch.epoch_people.add(*IDs)
								epoch.sources.add(*[x.id for x in newE.sources.all()])
								epoch.save()

					else:
						newPOCH_is_private = False
						if newE.event_is_private:
							newPOCH_is_private = True
						newPOCH = Epoch.objects.create(
							epoch_title = newE.event_title,
							created_by = request.user,
							epoch_type = newE.event_type,
							end_date = newE.event_date,
							end_date_approximate = newE.event_date_approximate,
							start_date_approximate = False,
							epoch_is_private = newPOCH_is_private
						)
						newPOCH.epoch_people.set(newE.event_people.all())
						newPOCH.sources.set(newE.sources.all())
						newPOCH.save()

				return redirect('event-details', event_id=newE.id)

	else:
		createeventform = CreateEventForm()
		context['createeventform'] = createeventform

	return render(request, 'private/events-add.html', context)



@login_required
def event_details(request, event_id):
	events = Event.objects.all().order_by('event_date')
	trgt = Event.objects.get(id=event_id)
	context = {
		'events': events,
		'targetE': trgt
	}
	if request.method == 'POST':
		if trgt.event_type == 'birth' or trgt.event_type == 'death' or trgt.event_type == 'im-/em-migration':
			eventeditform = EventEditFormA(request.POST)
		else:
			eventeditform = EventEditFormB(request.POST)
		context['eventeditform'] = eventeditform
		if eventeditform.is_valid():
			trgt.event_title = eventeditform.cleaned_data['event_title']
			trgt.event_description = eventeditform.cleaned_data['event_description']
			trgt.event_date = eventeditform.cleaned_data['event_date']
			trgt.event_date_approximate = eventeditform.cleaned_data['event_date_approximate']
			trgt.place = eventeditform.cleaned_data['place']
			trgt.sources.set(eventeditform.cleaned_data['sources'])
			if 'event_people' in request.POST:
				trgt.event_people.set(eventeditform.cleaned_data['event_people'])
			trgt.save()
			return redirect('event-details', event_id=event_id)	
	else:
		if trgt.event_type == 'birth' or trgt.event_type == 'death' or trgt.event_type == 'im-/em-migration':
			eventeditform = EventEditFormA(instance=trgt)
		else:
			eventeditform = EventEditFormB(instance=trgt)
		context['eventeditform'] = eventeditform

	return render(request, 'private/events-view.html', context)



@login_required
def epochs_landing(request):
	epochs = Epoch.objects.all().order_by('start_date')
	context = {
		'epochs':epochs
	}

	return render(request, 'private/epochs-welcome.html', context)



@login_required
def epoch_add(request):
	epochs = Epoch.objects.all().order_by('start_date')
	context = {
		'epochs':epochs
	}

	if request.method == 'POST':
		createepochform = CreateEpochForm(request.POST)
		context['createepochform'] = createepochform
		if createepochform.is_valid():
			epobj = Epoch.objects.create(
				created_by=request.user,
				epoch_title = createepochform.cleaned_data['epoch_title'],
				epoch_type = createepochform.cleaned_data['epoch_type'],
				epoch_description = createepochform.cleaned_data['epoch_description'],
				start_date = createepochform.cleaned_data['start_date'],
				start_date_approximate = createepochform.cleaned_data['start_date_approximate'],
				end_date = createepochform.cleaned_data['end_date'],
				end_date_approximate = createepochform.cleaned_data['end_date_approximate'],
				epoch_is_private = createepochform.cleaned_data['epoch_is_private']
			)
			epobj.epoch_people.set(createepochform.cleaned_data['epoch_people'])
			epobj.sources.set(createepochform.cleaned_data['sources'])
			epobj.save()
			return redirect('epoch-details', epoch_id=epobj.id)
			
	else:
		createepochform = CreateEpochForm()
		context['createepochform'] = createepochform

	return render(request, 'private/epoch-add.html', context)




@login_required
def epoch_details(request, epoch_id):
	epochs = Epoch.objects.all().order_by('start_date')
	trgtEP = Epoch.objects.get(id=epoch_id)
	context = {
		'epochs':epochs,
		'targetEP':trgtEP
	}

	if request.method == 'POST':
		epocheditform = EditEpochForm(request.POST)
		context['epocheditform'] = epocheditform
		if epocheditform.is_valid():
			trgtEP.epoch_title = epocheditform.cleaned_data['epoch_title']
			trgtEP.epoch_type = epocheditform.cleaned_data['epoch_type']
			trgtEP.epoch_description = epocheditform.cleaned_data['epoch_description']
			trgtEP.start_date = epocheditform.cleaned_data['start_date']
			trgtEP.start_date_approximate = epocheditform.cleaned_data['start_date_approximate']
			trgtEP.end_date = epocheditform.cleaned_data['end_date']
			trgtEP.end_date_approximate = epocheditform.cleaned_data['end_date_approximate']
			trgtEP.epoch_people.set(epocheditform.cleaned_data['epoch_people'])
			trgtEP.sources.set(epocheditform.cleaned_data['sources'])
			trgtEP.save()
			return redirect('epoch-details', epoch_id=trgtEP.id)
	else:
		epocheditform = EditEpochForm(instance=Epoch.objects.get(id=epoch_id), **{'Ruser': request.user})
		context['epocheditform'] = epocheditform

	return render(request, 'private/epoch-view.html', context)



@login_required
def nuggets_landing(request):
	BINs = BiographicalInfoNugget.objects.all().order_by('start_date')
	context = {
		'BINs': BINs
	}

	return render(request, 'private/nuggets-welcome.html', context)



@login_required
def nugget_add(request):
	BINs = BiographicalInfoNugget.objects.all().order_by('start_date')
	context = {
		'BINs': BINs
	}

	if request.method == 'POST':
		createnuggetform = CreateNuggetForm(request.POST)
		context['createnuggetform'] = createnuggetform
		if createnuggetform.is_valid():
			binobj = BiographicalInfoNugget.objects.create(
				title = createnuggetform.cleaned_data['title'],
				info = createnuggetform.cleaned_data['info'],
				start_date = createnuggetform.cleaned_data['start_date'],
				start_date_approximate = createnuggetform.cleaned_data['start_date_approximate'],
				end_date = createnuggetform.cleaned_data['end_date'],
				end_date_approximate = createnuggetform.cleaned_data['end_date_approximate'],
				created_by = request.user,
				nugget_is_private = createnuggetform.cleaned_data['nugget_is_private']
			)
			binobj.people.set(createnuggetform.cleaned_data['people'])
			binobj.sources.set(createnuggetform.cleaned_data['sources'])
			binobj.save()
			return redirect('nugget-details', nugget_id=binobj.id)
	else:
		createnuggetform = CreateNuggetForm()
		context['createnuggetform'] = createnuggetform

	return render(request, 'private/nugget-add.html', context)



@login_required
def nugget_details(request, nugget_id):
	BINs = BiographicalInfoNugget.objects.all().order_by('start_date')
	trgt = BiographicalInfoNugget.objects.get(id=nugget_id)
	context = {
		'BINs': BINs,
		'targetNUG': trgt
	}
	if request.method == 'POST':
		editnuggetform = EditNuggetForm(request.POST)
		context['editnuggetform'] = editnuggetform
		if editnuggetform.is_valid():
			trgt.title = editnuggetform.cleaned_data['title']
			trgt.info = editnuggetform.cleaned_data['info']
			trgt.start_date = editnuggetform.cleaned_data['start_date']
			trgt.start_date_approximate = editnuggetform.cleaned_data['start_date_approximate']
			trgt.end_date = editnuggetform.cleaned_data['end_date']
			trgt.end_date_approximate = editnuggetform.cleaned_data['end_date_approximate']
			trgt.people.set(editnuggetform.cleaned_data['people'])
			trgt.sources.set(editnuggetform.cleaned_data['sources'])
			trgt.save()
			return redirect('nugget-details', nugget_id=trgt.id)
	else:
		editnuggetform = EditNuggetForm(instance=trgt)
		context['editnuggetform'] = editnuggetform

	return render(request, 'private/nugget-view.html', context)



@login_required
def relationships_landing(request):
	RELs = Relationship.objects.all().order_by('start_date')
	context = {
		'RELs': RELs
	}
	
	return render(request, 'private/relationships-welcome.html', context)




BIDIRECTIONAL_RELATIONSHIP = {
	'parent of': 'child of',
	'child of': 'parent of',
	'spouse of': 'spouse of',
	'guardian of': 'ward of',
	'ward of': 'guardian of'
}
@login_required
def relationship_add(request):
	RELs = Relationship.objects.all().order_by('start_date')
	context = {
		'RELs': RELs
	}
	if request.method == 'POST':
		createrelationshipform = CreateRelationshipForm(request.POST)
		context['createrelationshipform'] = createrelationshipform
		if createrelationshipform.is_valid():
			newRel = Relationship.objects.create(
				created_by = request.user,
				principle = createrelationshipform.cleaned_data['principle'],
				relationship_type = createrelationshipform.cleaned_data['relationship_type'],
				referent = createrelationshipform.cleaned_data['referent'],
				start_date = createrelationshipform.cleaned_data['start_date'],
				start_date_approximate = createrelationshipform.cleaned_data['start_date_approximate'],
				end_date = createrelationshipform.cleaned_data['end_date'],
				end_date_approximate = createrelationshipform.cleaned_data['end_date_approximate'],
				relationship_is_private = createrelationshipform.cleaned_data['relationship_is_private']
			)
			newRel.sources.set(createrelationshipform.cleaned_data['sources'])
			newRel.save()

			bidRel = Relationship.objects.create(
				created_by = request.user,
				principle = createrelationshipform.cleaned_data['referent'],
				relationship_type = BIDIRECTIONAL_RELATIONSHIP[createrelationshipform.cleaned_data['relationship_type']],
				referent = createrelationshipform.cleaned_data['principle'],
				start_date = createrelationshipform.cleaned_data['start_date'],
				start_date_approximate = createrelationshipform.cleaned_data['start_date_approximate'],
				end_date = createrelationshipform.cleaned_data['end_date'],
				end_date_approximate = createrelationshipform.cleaned_data['end_date_approximate'],
				relationship_is_private = createrelationshipform.cleaned_data['relationship_is_private']
			)
			bidRel.sources.set(createrelationshipform.cleaned_data['sources'])
			bidRel.save()

			bidRel.bidirrel = newRel
			bidRel.save()
			newRel.bidirrel = bidRel
			newRel.save()

			return redirect('relationship-details', relationship_id=newRel.id)

	else:
		createrelationshipform = CreateRelationshipForm()
		context['createrelationshipform'] = createrelationshipform
	
	return render(request, 'private/relationship-add.html', context)


@login_required
def relationship_details(request, relationship_id):
	RELs = Relationship.objects.all().order_by('start_date')
	trgt = Relationship.objects.get(id=relationship_id)
	context = {
		'RELs': RELs,
		'targetREL': trgt
	}
	if request.method == 'POST':
		editrelationshipform = EditRelationshipForm(request.POST)
		context['editrelationshipform'] = editrelationshipform
		if editrelationshipform.is_valid():
			trgt.start_date = editrelationshipform.cleaned_data['start_date']
			trgt.start_date_approximate = editrelationshipform.cleaned_data['start_date_approximate']
			trgt.end_date = editrelationshipform.cleaned_data['end_date']
			trgt.end_date_approximate = editrelationshipform.cleaned_data['end_date_approximate']
			trgt.sources.set(editrelationshipform.cleaned_data['sources'])
			trgt.save()

			if trgt.bidirrel:
				trgtbidirrel = Relationship.objects.get(id=trgt.bidirrel.id)
				trgtbidirrel.start_date = editrelationshipform.cleaned_data['start_date']
				trgtbidirrel.start_date_approximate = editrelationshipform.cleaned_data['start_date_approximate']
				trgtbidirrel.end_date = editrelationshipform.cleaned_data['end_date']
				trgtbidirrel.end_date_approximate = editrelationshipform.cleaned_data['end_date_approximate']
				trgtbidirrel.sources.set(editrelationshipform.cleaned_data['sources'])
				trgtbidirrel.save()
			
			return redirect('relationship-details', relationship_id=trgt.id)

	else:
		editrelationshipform = EditRelationshipForm(instance=trgt)
		context['editrelationshipform'] = editrelationshipform
	
	return render(request, 'private/relationship-view.html', context)



@login_required
def visualizations_landing(request):
	context = {}
	return render(request, 'private/visualizations-welcome.html', context)