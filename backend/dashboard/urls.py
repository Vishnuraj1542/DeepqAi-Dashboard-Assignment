from django.urls import path
from .views import IndicatorListView,LoginView,LogoutView,RegistrationView,FetchWorldBankData

urlpatterns=[
    path('registration/',RegistrationView.as_view(),name = 'register-user'),
    path('login/',LoginView.as_view(),name='login-user'),
    path('logout/',LogoutView.as_view(),name='logout-user'),

    path('indicators/',IndicatorListView.as_view(),name='indicator-view-list'),
    path('fetch-data/',FetchWorldBankData.as_view(),name = 'fetch-data')
]