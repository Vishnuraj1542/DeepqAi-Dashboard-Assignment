from django.urls import path
from .views import IndicatorListView,LoginView,LogoutView,RegistrationView,FetchWorldBankData,DashboardView

urlpatterns=[
    path('registration/',RegistrationView.as_view(),name = 'register-user'),
    path('',LoginView.as_view(),name='login-user'),
    path('logout/',LogoutView.as_view(),name='logout-user'),

    path('dashboard/',DashboardView.as_view(),name='dashboard-view'),
    path('indicators/',IndicatorListView.as_view(),name='indicator-view-list'),
    # path("fetch-user/", FetchUserView.as_view(), name="fetch-user"),
    path('fetch-data/',FetchWorldBankData.as_view(),name = 'fetch-data')

]