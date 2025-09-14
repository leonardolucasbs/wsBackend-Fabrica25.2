from .api.viewset import UsuariosViewSet, LivrosViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *


router = DefaultRouter()
router.register(r'usuarios', UsuariosViewSet, basename='usuarios')
router.register(r'livros', LivrosViewSet, basename='livros')

urlpatterns = [
    path('cadastro/', cadastroUsuario.as_view(), name='cadastroUsuario'),
    path('', loginUsuario.as_view(), name='loginUsuario'),
    path("alugar/", alugarLivro, name="alugarLivro"),
    path("locacoes/", locacoes, name="locacoes"),
    path("home/", listaDeLivros, name="home"),
    path("logout/", logout, name="logout"),
    path('api/', include(router.urls)),

]