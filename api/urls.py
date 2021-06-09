from django.urls import path
from . import views

urlpatterns = [
    path('puskesmas/', views.PuskesmasView.as_view(), name='puskesmas-index'),
    path('puskesmas/<str:id_puskesmas>', views.PuskesmasDetailView.as_view(), name='puskesmas-detail'),
    path('user/', views.UserView.as_view(), name='user-index'),
    path('user/<str:id_user>', views.UserDetailView.as_view(), name='user-detail'),
    path('user/<str:id_user>/prescription/', views.PrescriptionFilterUserView.as_view(), name='prescription-user-index'),
    path('user/<str:id_user>/treatment/', views.TreatmentFilterUserView.as_view(), name='treatment-user-index'),
    path('hospital/', views.HospitalView.as_view(), name='hospital-index'),
    path('hospital/<str:id_hospital>', views.HospitalDetailView.as_view(), name='hospital-detail'),
    path('treatment/', views.TreatmentView.as_view(), name='treatment-index'),
    path('treatment/<str:id_treatment>', views.TreatmentDetailView.as_view(), name='treatment-detail'),
    path('covid-data/', views.CovidDataView.as_view(), name='covidData-index'),
    path('prescription/', views.PrescriptionView.as_view(), name='prescription-index'),
    path('prescription/<str:id_prescription>', views.PrescriptionDetailView.as_view(), name='prescription-detail'),
    path('banner/', views.BannerHeaderView.as_view(), name='banner-index'),
    path('article/', views.ArticleView.as_view(), name='article-index'),
    path('article/<str:id_article>', views.ArticleDetailView.as_view(), name='article-detail'),
]
