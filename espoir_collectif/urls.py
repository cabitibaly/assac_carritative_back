from django.urls import path
from .views import *

urlpatterns = [
    path('api/register/',register, name='register'),
    path('api/login/', login, name='login'),
    path('api/logout/', logout, name='logout'),
    path('api/user/', getUser, name='getUser'),
    path('api/user/modifier', updateUser, name='updateUser'),
    path('api/creer_cagnotte/',creer_cagnotte, name='creer_cagnotte'),
    path('api/cagnottes/', liste_cagnottes, name='liste_cagnottes'),
    path('api/cagnottes/user', user_cagnottes, name='user_cagnottes'),
    path('api/cagnottes/<int:cagnotte_id>', details_cagnotte, name='details_cagnotte'),
    path('api/cagnottes/search/<str:terme>', rechercher_cagnotte, name='rechercher_cagnotte'),
    path('api/faire_don/<int:cagnotte_id>', faire_don, name='faire_don'),
]

