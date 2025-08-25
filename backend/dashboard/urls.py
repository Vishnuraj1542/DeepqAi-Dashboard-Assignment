from django.urls import path
from .views import IndicatorDetailView,IndicatorListCreateView,UserListView

urlpatterns=[
    path('users/',UserListView.as_view(),name='users-list'),
    path('indicators/',IndicatorListCreateView(),name='indicator-create-list'),
    path('indicator/<int:id>/',IndicatorDetailView(),name='indicator-detail')
]