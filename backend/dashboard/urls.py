from django.urls import path
from .views import IndicatorDetailView,IndicatorListCreateView,UserListView,LoginView,LogoutView,RegistrationView,FetchWorldBankData

urlpatterns=[
    path('registration/',RegistrationView.as_view(),name = 'register-user'),
    path('login/',LoginView.as_view(),name='login-user'),
    path('logout/',LogoutView.as_view(),name='logout-user'),

    path('users/',UserListView.as_view(),name='users-list'),
    path('indicators/',IndicatorListCreateView.as_view(),name='indicator-create-list'),
    path('indicator/<int:id>/',IndicatorDetailView.as_view(),name='indicator-detail'),

    path('fetch-data/',FetchWorldBankData.as_view(),name = 'fetch-data')
]