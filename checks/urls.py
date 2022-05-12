from django.urls import path

from checks.views import CheckListView

urlpatterns = [path('checks/', CheckListView.as_view()), ]
