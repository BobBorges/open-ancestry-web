from django.urls import path
from . import views as private_views





urlpatterns = [
	# EPOCHS
	path('epochs/', private_views.epochs_landing, name='epochs-landing'),
	path('epochs/epoch/add/', private_views.epoch_add, name='epoch-add'),
	path('epochs/epoch/<str:epoch_id>/', private_views.epoch_details, name='epoch-details'),
	# EVENTS
	path('events/', private_views.events_landing, name='events-landing'),
	path('events/event/add/', private_views.event_add, name='event-add'),
	path('events/event/<str:event_id>/', private_views.event_details, name='event-details'),
	# NUGGETS
	path('nuggets/', private_views.nuggets_landing, name='nuggets-landing'),
	path('nuggets/nugget/add/', private_views.nugget_add, name='nugget-add'),
	path('nuggets/nugget/<str:nugget_id>/', private_views.nugget_details, name='nugget-details'),
	# PEOPLE
	path('people/', private_views.people_landing, name='people-landing'),
	path('people/person/add/', private_views.person_add, name='person-add'),
	path('people/person/<str:principle_id>/', private_views.person_details, name='person-details'),
	# RELATIONSHIPS
	path('relationships/', private_views.relationships_landing, name='relationships-landing'),
	path('relationships/relationship/add/', private_views.relationship_add, name='relationship-add'),
	path('relationships/relationship/<str:relationship_id>/', private_views.relationship_details, name='relationship-details'),
	# SOURCES
	path('sources/', private_views.sources_landing, name='sources-landing'),
	path('sources/source/add/', private_views.source_add, name='source-add'),
	path('sources/source/<str:source_id>/', private_views.source_details, name='source-details'),
	path('visualizations/', private_views.visualizations_landing, name='visualizations-landing'),

]