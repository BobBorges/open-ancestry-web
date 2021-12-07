from django.contrib.auth.models import User
from django.db import models
import os, string, random



DATE_HELP = "YYYY-MM-DD. Approximate dates can also be given in YYYY-MM or YYYY format. In this case, tick the below 'Start | End date approximate' box."
SOURCE_TYPE_OPTS = (
	('document (primary source)', 'document (primary source)'),
	('document (secondary source)', 'document (secondary source)'),
	('image (photograph / painting)', 'image (photograph / painting)'),
	('other', 'other')
)
class Source(models.Model):
	source_title = models.CharField(max_length=510)
	created_in_DB = models.DateTimeField(auto_now_add=True)
	created_in_DB_by_user = models.ForeignKey(User, on_delete=models.PROTECT)
	source_type = models.CharField(max_length=255, choices=SOURCE_TYPE_OPTS)
	source_file = models.FileField(upload_to='priv/')
	source_creator = models.CharField(max_length=510, blank=True)
	source_date_of_creation = models.CharField(max_length=255, help_text=DATE_HELP, blank=True)
	source_DOC_approximate = models.BooleanField()
	source_description = models.TextField()
	source_bibliographic_reference = models.TextField(blank=True)
	src_is_private = models.BooleanField()

	def __str__(self):
		return self.source_title




SEX_OPTS = (
	('male', 'male'),
	('female', 'female')
)
class Person(models.Model):
	created = models.DateTimeField('created', auto_now_add=True)
	created_by_user = models.ForeignKey(User, on_delete=models.PROTECT)
	given_name = models.CharField(max_length=255)
	surname_at_birth = models.CharField(max_length=255)
	sex = models.CharField(max_length=255, choices=SEX_OPTS)
	living = models.BooleanField()
	headshot = models.ForeignKey(
		Source, 
		related_name='headhshot', 
		on_delete=models.PROTECT, 
		blank=True, 
		null=True
	)
	sources = models.ManyToManyField(Source, related_name='sources', blank=True)

	class Meta:
		verbose_name = "Person"
		verbose_name_plural = "People"
		ordering = ['surname_at_birth']

	def __str__(self):
		return f'{self.surname_at_birth}, {self.given_name}'




ALTERNATIVE_TYPES = (
	('nickname, or non-legal a.k.a.', 'nickname, or non-legal a.k.a.'),
	('legal change due to marriage', 'legal change due to marriage'),
	('legal change due to immigration', 'legal change due to immigration'),
	('other', 'other')
)
class AlternativeName(models.Model):
	principle = models.ForeignKey(Person, on_delete=models.PROTECT)
	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.PROTECT)
	alternate_first = models.CharField(max_length=255, blank=True)
	alternate_surname = models.CharField(max_length=255, blank=True)
	alternative_type = models.CharField(max_length=255, choices=ALTERNATIVE_TYPES)
	explanation = models.TextField(blank=True)
	start_date_of_alternative = models.CharField(max_length=255, help_text=DATE_HELP, blank=True)
	start_date_approximate = models.BooleanField()
	end_date_of_alternative = models.CharField(max_length=255, help_text=DATE_HELP, blank=True)
	end_date_approximate = models.BooleanField()
	sources  = models.ManyToManyField(Source, blank=True)




EVENT_TYPES = (
	('birth', 'birth'),
	('death', 'death'),
	('baptism', 'baptism'),
	('marriage', 'marriage'), # (triggers relationship and epoch)
	('divorce', 'divorce'), # (ends marriage epoch)
	('im-/em-migration', 'im-/em-migration'), # (triggers end and start of new epoch)
	('other', 'other')
)
PLACE_HELP = "Indicate places from non-specifiic to specific as possible from left to right. Country --> state/province --> municipality --> city/town --> address. E.g. USA, Rhode Island, Providence, 105 North Main st."
class Event(models.Model):
	event_title = models.CharField(max_length=510)
	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.PROTECT)
	event_type = models.CharField(max_length=255, choices=EVENT_TYPES)	
	event_description = models.TextField(blank=True)
	event_date = models.CharField(max_length=255, help_text=DATE_HELP, blank=True)
	event_date_approximate = models.BooleanField()
	event_people = models.ManyToManyField(Person)
	place = models.CharField(max_length=1020, help_text=PLACE_HELP, blank=True)
	sources = models.ManyToManyField(Source, blank=True)
	event_is_private = models.BooleanField()

	def __str__(self):
		return self.event_title




EPOCH_TYPES = (
	('residence', 'residence'),
	('study / work', 'study / work'),
	('marriage', 'marriage'),
	('other','other')
)
class Epoch(models.Model):
	epoch_title = models.CharField(max_length=510)
	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.PROTECT)
	epoch_type = models.CharField(max_length=255, choices=EPOCH_TYPES)
	epoch_description = models.TextField(blank=True)
	start_date = models.CharField(max_length=255, help_text=DATE_HELP, blank=True)
	start_date_approximate = models.BooleanField()
	end_date = models.CharField(max_length=255, help_text=DATE_HELP, blank=True)
	end_date_approximate = models.BooleanField()
	epoch_people = models.ManyToManyField(Person)
	sources = models.ManyToManyField(Source, blank=True)
	epoch_is_private = models.BooleanField()

	def __str__(self):
		return self.epoch_title



RELATIONSHIP_TYPES = (
	# biological 
	('parent of', 'parent of'),
	('child of', 'child of'),
	# affinal | classificatory
	('spouse of', 'spouse of'), # (triggers event and epoch)
	('guardian of', 'guardian of'),
	('ward of', 'ward of')
)
RELATIONSHIP_DATE_HELP = "Biological relationships start on the birth day of the child – no end date is necessary. Date information for non-biological relationships should be entered based on a marriage / adoption event. And end date should be entered for 'spouse of' relatonships in the case of divorce, or for 'guardian/ward' relationships if/when there is a clear end to that relationship."
class Relationship(models.Model):
	principle = models.ForeignKey(Person, related_name='principle', on_delete=models.PROTECT)
	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.PROTECT)		
	relationship_type = models.CharField(max_length=255, choices=RELATIONSHIP_TYPES)
	referent = models.ForeignKey(Person, related_name='referent', on_delete=models.PROTECT)
	start_date = models.CharField(
		max_length=255, 
		help_text=f'{DATE_HELP} {RELATIONSHIP_DATE_HELP}', 
		blank=True
	)
	start_date_approximate = models.BooleanField()
	end_date = models.CharField(
		max_length=255,
	 	help_text=f'{DATE_HELP} {RELATIONSHIP_DATE_HELP}' , 
	 	blank=True
 	)
	end_date_approximate = models.BooleanField()
	bidirrel = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)
	sources = models.ManyToManyField(Source, blank=True)
	relationship_is_private = models.BooleanField()

	def __str__(self):
		return f'{self.principle} {self.relationship_type} {self.referent}'


class BiographicalInfoNugget(models.Model):
	title = models.CharField(max_length=510)
	info = models.TextField()
	start_date = models.CharField(max_length=255, help_text=DATE_HELP, blank=True)
	start_date_approximate = models.BooleanField()
	end_date = models.CharField(max_length=255, help_text=DATE_HELP, blank=True)
	end_date_approximate = models.BooleanField()
	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.PROTECT)	
	people = models.ManyToManyField(Person)
	sources = models.ManyToManyField(Source, blank=True)
	nugget_is_private = models.BooleanField()

	def __str__(self):
		return self.title




RESEARCH_TYPES = (
	('question', 'question'),
	('theory', 'theory'),
	('dead end', 'dead end')
)
class Research(models.Model):
	title = models.CharField(max_length=510)
	item_type = models.CharField(max_length=255, choices=RESEARCH_TYPES)
	principle = models.ForeignKey(Person, on_delete=models.PROTECT)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.PROTECT)
	research_is_private = models.BooleanField()
	active = models.BooleanField()
	
	def __str__(self):
		return self.title



class ResearchReply(models.Model):
	reply_to = models.ForeignKey(Research, on_delete=models.PROTECT)
	created = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, on_delete=models.PROTECT)
	content = models.TextField()