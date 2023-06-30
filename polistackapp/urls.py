from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path("congress/bills/", views.congress_view, name='congress_bills'),
    path('congress/bill/<str:bill_id>/', views.bill_detail, name='bill_detail')
]