from django.urls import path
from polls import views as views

urlpatterns = [
    # path("", views.index, name="index"),
    path("create_deal/", views.create_deal, name = "create_deal"),
    path("claim_deal/", views.claim_deal, name = 'claim_deal')
]