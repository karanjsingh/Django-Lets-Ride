from django.urls import path
from . import views
# from .views import addTemClass
urlpatterns = [
    path('request/', views.requester_index, name='request'),
    path('rider/', views.rider_index, name='rider'),
    path('riderreq/',views.rider_entry ,name='riderreq'),
    path('req/',views.req_entry ,name='req'),
    path('showrider/',views.showRiderData ,name='showrider'),
    path('showrequest/',views.showRequestData ,name='showrequest'),
    path('showallrider/',views.showAllRiderData ,name='showallrider'),    
    
]
