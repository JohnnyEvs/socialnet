from django.urls import path
from .views import *

urlpatterns = [
    # path('registration/', register, name='register'),
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
]



