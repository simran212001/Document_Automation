from django.urls import path
from . import views

urlpatterns = [

    path('home/',views.home, name='home'),
    path('Context_dia/',views.Context_dia, name='Context'),
    path('create_graph/',views. create_graph, name=' create_graph'),
    path('UseCase_dia/',views.UseCase_dia, name='UseCase'),
    path('ERD/',views.ERD, name='ERD'),
    path('notify/', views.notify, name='notify'),
]
