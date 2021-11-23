from django import forms
from django.forms import ModelForm
from .models import ResearchReply, Research, Person, Source, Event, Epoch, BiographicalInfoNugget, Relationship, AlternativeName







#####################
# ALTERNATIVE NAMES #
#####################
class CreateAlternativeNameForm(forms.ModelForm):

	class Meta:
		model = AlternativeName
		fields = ['alternate_first', 'alternate_surname', 'alternative_type', 'explanation', 'start_date_of_alternative', 'start_date_approximate', 'end_date_of_alternative', 'end_date_approximate', 'sources']




class EditAlternativeNameForm(forms.ModelForm):

	ANIDfield = forms.CharField(max_length=255)

	class Meta:
		model = AlternativeName
		fields = ['alternate_first', 'alternate_surname', 'alternative_type', 'explanation', 'start_date_of_alternative', 'start_date_approximate', 'end_date_of_alternative', 'end_date_approximate', 'sources']



#########
# EPOCH #
#########
class CreateEpochForm(forms.ModelForm):

	class Meta:
		model = Epoch
		fields = ['epoch_title', 'epoch_type', 'epoch_description', 'start_date', 'start_date_approximate', 'end_date', 'end_date_approximate', 'epoch_people', 'sources', 'epoch_is_private']



class EditEpochForm(forms.ModelForm):

	class Meta:
		model = Epoch
		fields = ['epoch_title', 'epoch_type', 'epoch_description', 'start_date', 'start_date_approximate', 'end_date', 'end_date_approximate', 'epoch_people', 'sources', 'epoch_is_private']
	
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('Ruser', None)
		super(EditEpochForm, self).__init__(*args, **kwargs)
		
		if user != self.instance.created_by:
			print("YAAAH")
			self.fields.pop('epoch_is_private')
		




		
##########
# EVENTS #
##########
class CreateEventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['event_title', 'event_type', 'event_date', 'event_date_approximate', 'place', 'event_people', 'event_description', 'sources', 'event_is_private']




class EventEditFormA(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['event_title', 'event_description', 'event_date', 'event_date_approximate', 'place', 'sources']




class EventEditFormB(forms.ModelForm):

	class Meta:
		model = Event
		fields = ['event_title', 'event_description', 'event_date', 'event_date_approximate', 'event_people', 'place', 'sources']




###########
# NUGGETS #
###########
class CreateNuggetForm(forms.ModelForm):

	class Meta:
		model = BiographicalInfoNugget
		fields = ['title', 'info', 'start_date', 'start_date_approximate', 'end_date', 'end_date_approximate', 'people', 'sources', 'nugget_is_private']




class EditNuggetForm(forms.ModelForm):

	class Meta:
		model = BiographicalInfoNugget
		fields = ['title', 'info', 'start_date', 'start_date_approximate', 'end_date', 'end_date_approximate', 'people', 'sources']




##########
# PEOPLE #
##########
class CreatePersonForm(forms.ModelForm):

	class Meta:
		model = Person
		fields = ['given_name', 'surname_at_birth', 'sex', 'living', 'headshot', 'sources']




class PersonEditForm(forms.ModelForm):

	class Meta:
		model = Person
		fields = ['given_name', 'surname_at_birth', 'sex', 'living', 'headshot', 'sources']




#################
# RELATIONSHIPS #
#################
class CreateRelationshipForm(forms.ModelForm):

	class Meta:
		model = Relationship
		fields = ['principle', 'relationship_type', 'referent', 'start_date', 'start_date_approximate', 'end_date', 'end_date_approximate', 'sources', 'relationship_is_private']




class EditRelationshipForm(forms.ModelForm):

	class Meta:
		model = Relationship
		fields = ['start_date', 'start_date_approximate', 'end_date', 'end_date_approximate', 'sources']




############
# RESEARCH #
############
class ReplyForm(forms.ModelForm):

	content = forms.CharField(widget=forms.Textarea, label=False)

	class Meta:
		model = ResearchReply
		fields = ['content']




class ResearchForm(forms.ModelForm):

	content = forms.CharField(widget=forms.Textarea, label=False)

	class Meta:
		model = Research
		fields = ['title', 'item_type', 'content', 'research_is_private']




###########
# SOURCES #
###########
class CreateSourceForm(forms.ModelForm):

	class Meta:
		model = Source
		fields = ['source_title', 'source_type', 'source_file', 'source_creator', 'source_date_of_creation', 'source_DOC_approximate', 'source_description', 'source_bibliographic_reference', 'src_is_private']




class SourceEditForm(forms.ModelForm):

	class Meta:
		model = Source
		fields = ['source_title', 'source_type', 'source_creator', 'source_date_of_creation', 'source_DOC_approximate', 'source_description', 'source_bibliographic_reference', 'src_is_private']



