from django.urls import path
from .views import *


urlpatterns = [

    path('', HelloWord.as_view(), name='hello-world')


]