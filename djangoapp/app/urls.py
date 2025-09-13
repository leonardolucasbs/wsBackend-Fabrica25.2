from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.viewsets import UsuariosViewSet, LivrosViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuariosViewSet)
router.register(r'livros', LivrosViewSet)

urlpatterns = [
    path('', include(router.urls)),
]