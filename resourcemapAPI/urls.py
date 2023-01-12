from django.urls import path
from . import views
# from .views import addTemClass
urlpatterns = [
    path('requests/', views.getRequestData),
    path('rides/', views.getRiderData),
    path('addreq/', views.addrequest, name="addreq"),
    path('addride/', views.addrider),
    path('mapresource/', views.mapResource),
    path('clear/', views.clear),
    path('allriders/',views.getAllRiderData),
    

]
