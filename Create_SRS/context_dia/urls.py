from django.urls import path
from . import views
from .views import GeneratePDF
urlpatterns = [
    # path('',views.home1,name = 'home1'),
    path('home/',views.home, name='home'),
    path('Context_dia/',views.Context_dia, name='Context'),
    path('create_graph/',views. create_graph, name=' create_graph'),
    path('UseCase_dia/',views.UseCase_dia, name='UseCase'),
    path('ERD/',views.ERD, name='ERD'),
    path('notify/', views.notify, name='notify'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate_pdf/<int:pdf_report_id>/', views.GeneratePDF.as_view(), name='generate_pdf'),
     path('dfd/', views.generate_dfd, name='generate_dfd'),
]
