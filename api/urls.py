from django.urls import path
from . import views

urlpatterns = [
    path('puskesmas/', views.PuskesmasView.as_view(), name='puskesmas-index'),
    path('puskesmas/<str:id_puskesmas>', views.PuskesmasDetailView.as_view(), name='puskesmas-detail'),
    path('user/', views.UserView.as_view(), name='user-index'),
    path('user/<str:id_user>', views.UserDetailView.as_view(), name='user-detail'),
]
