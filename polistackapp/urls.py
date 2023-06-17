from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path("congress/bills/", views.congress_view)
]