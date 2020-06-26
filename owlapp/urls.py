from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.index, name='index'),
    path('submit', views.submit, name='submit'),
    path('problems', views.problems, name='problems'),
    path('problems/<int:id>', views.problempage, name='problempage'),
    path('results', views.subresults, name='results'),
    path('judgecode', views.judge, name='judge'),
    path('submissions', views.submissions, name='submissions'),
    path("login", views.login_user),
    path('logout', views.logout_view, name='logout'),
    path('result/<int:id>', views.result, name='problempage'),
    path("registration", views.registation_user)
]
