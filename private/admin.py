from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import *








class PersonAdmin(VersionAdmin):
	fields = [
#		'created', 
		'created_by_user', 
		'given_name',
		'headshot',
		'surname_at_birth',
		'sex',
		'living',
		'sources'
	]
	list_display = (
		'surname_at_birth', 
		'given_name',
		'created', 
		'created_by_user',
		'sex', 
		'living',
		'sources_list'
	)

	def sources_list(self, obj):
		return "\n".join([s.source_title for s in obj.sources.all()])




class AlternativeNameAdmin(VersionAdmin):
	fields = [
		'created_by',
		'principle', 
		#'created',	
		'alternate_first',
		'alternate_surname',
		'alternative_type',
		'explanation',
		'start_date_of_alternative',
		'start_date_approximate',		
		'end_date_of_alternative',
		'end_date_approximate',
		'sources'
	]
	list_display = (
		'principle', 
		'alternate_surname',
		'alternate_first',
		'alternative_type',
		'explanation',
		'start_date_of_alternative',
		'start_date_approximate',		
		'end_date_of_alternative',
		'end_date_approximate',
		'sources_list',
		'created',	
		'created_by'
	)

	def sources_list(self, obj):
		return "\n".join([s.source_title for s in obj.sources.all()])




class EventAdmin(VersionAdmin):
	fields  = [
		'created_by',
		'event_title',
		#'created',
		'event_type',
		'event_description',
		'event_date',
		'event_date_approximate',
		'event_people',
		'place',
		'sources',
		'event_is_private'
	]
	list_display = (
		'event_title',
		'event_type',
		'event_description',
		'people_list',
		'event_date',
		'event_date_approximate',
		'place',
		'sources_list',
		'created',
		'created_by',
		'event_is_private'
	)

	def sources_list(self, obj):
		return "\n".join([s.source_title for s in obj.sources.all()])

	def people_list(self, obj):
		return "\n".join([f'{p.surname_at_birth}, {p.given_name}' for p in obj.event_people.all()])




class EpochAdmin(VersionAdmin):
	fields = [
		'created_by',
		'epoch_title',
		#'created',
		'epoch_type',
		'epoch_description',
		'start_date',
		'start_date_approximate',
		'end_date',
		'end_date_approximate',
		'epoch_people',
		'sources',
		'epoch_is_private'
	]
	list_display = (
		'epoch_title',
		'epoch_type',
		'people_list',
		'epoch_description',
		'start_date',
		'start_date_approximate',
		'end_date',
		'end_date_approximate',
		'sources_list',
		'created',
		'created_by',
		'epoch_is_private'
	)

	def sources_list(self, obj):
		return "\n".join([s.source_title for s in obj.sources.all()])

	def people_list(self, obj):
		return "\n".join([f'{p.surname_at_birth}, {p.given_name}' for p in obj.epoch_people.all()])




class RelationshipAdmin(VersionAdmin):
	fields= [
		'created_by',
		'principle',
		#'created',
		'relationship_type',
		'referent',
		'start_date',
		'start_date_approximate',
		'end_date',
		'end_date_approximate',
		'bidirrel',		
		'sources',
		'relationship_is_private'
	]
	list_display = (
		'principle',
		'relationship_type',
		'referent',
		'start_date',
		'start_date_approximate',
		'end_date',
		'end_date_approximate',
		'sources_list',
		'bidirrel',
		'created',
		'created_by',
		'relationship_is_private'
	)

	def sources_list(self, obj):
		return "\n".join([s.source_title for s in obj.sources.all()])




class SourceAdmin(VersionAdmin):
	list_display = [
		'source_title',
		'source_type',
		'source_description',
		'source_file',
		'source_creator',
		'source_date_of_creation',
		'source_DOC_approximate',
		'source_bibliographic_reference',
		'created_in_DB',
		'created_in_DB_by_user',
		'src_is_private'
	]




class BINAdmin(VersionAdmin):
	fields = [
		'created_by',
		'title',
		'info',
		'start_date',
		'start_date_approximate',
		'end_date',
		'end_date_approximate',
		#'created',
		'people',
		'sources',
		'nugget_is_private'
	]
	list_display = (
		'title',
		'info',
		'start_date',
		'start_date_approximate',
		'end_date',
		'end_date_approximate',
		'created',
		'created_by',
		'people_list',
		'sources_list',
		'nugget_is_private'
	)

	def sources_list(self, obj):
		return "\n".join([s.source_title for s in obj.sources.all()])

	def people_list(self, obj):
		return "\n".join([f'{p.surname_at_birth}, {p.given_name}' for p in obj.people.all()])




class ResearchAdmin(admin.ModelAdmin):
	fields = [
		'created_by',
		'title',
		'item_type',
		'principle',
		'content',
		#'created',

	 	'research_is_private',
	 	'active'
	]
	list_display = (
		'title',
		'item_type',
		'principle',
		'content',
		'created',
		'created_by',
	 	'research_is_private',
	 	'active'
	)




class ResearchReplyAdmin(admin.ModelAdmin):
	fields = [
		'created_by',
		'reply_to',
		#'created',
		'content'
	]
	list_display = (
		'reply_to',
		'created',
		'created_by',
		'content'
	)




admin.site.register(Person, PersonAdmin)
admin.site.register(AlternativeName, AlternativeNameAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Epoch, EpochAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(BiographicalInfoNugget, BINAdmin)
admin.site.register(Research, ResearchAdmin)
admin.site.register(ResearchReply, ResearchReplyAdmin)