from django.urls import path
from . import views

urlpatterns = [
    path('puskesmas/', views.PuskesmasView.as_view(), name='puskesmas-index'),
    path('puskesmas/<str:id_puskesmas>', views.PuskesmasDetailView.as_view(), name='puskesmas-detail'),
    path('user/', views.UserView.as_view(), name='user-index'),
    path('user/<str:id_user>', views.UserDetailView.as_view(), name='user-detail'),
    path('hospital/', views.HospitalView.as_view(), name='hospital-index'),
    path('hospital/<str:id_hospital>', views.HospitalDetailView.as_view(), name='hospital-detail'),
    path('treatment/', views.TreatmentView.as_view(), name='treatment-index'),
    # path('treatment/<str:id_treatment>', views.TreatmentDetailView.as_view(), name='treatment-detail'),
]
