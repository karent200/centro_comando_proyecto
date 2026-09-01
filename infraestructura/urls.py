from django.urls import path
from .views import lista_servidores

urlpatterns = [
    path('', lista_servidores, name='home_servidores'),
]