from django.urls import path
from . import views
from core.views import HomePageView, SamplePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('sample/',SamplePageView.as_view(), name='sample'),
]
