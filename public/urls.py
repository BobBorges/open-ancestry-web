from django.urls import path
from . import views as public_views




urlpatterns = [
	path('', public_views.landing_page, name='landing-page'),
	path('statistics/', public_views.statistics, name='statistics-page'),
	path('about/', public_views.about, name='about-page')
]