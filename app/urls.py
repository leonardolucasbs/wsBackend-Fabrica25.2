from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.viewset import UsuariosViewSet, LivrosViewSet
from .views import *


router = DefaultRouter()
router.register(r'usuarios', UsuariosViewSet)
router.register(r'livros', LivrosViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('cadastro/', cadastroUsuario.as_view(), name='cadastroUsuario'),
    path("home/", listaDeLivros, name="home"),

]