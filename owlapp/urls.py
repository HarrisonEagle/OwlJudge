from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('problems', views.problems, name='problems'),
    path('results', views.subresults, name='results'),
    path('judgecode', views.judge, name='judge')
]
