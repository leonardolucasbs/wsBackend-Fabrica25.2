# app/api/viewset.py
from .serializers import LivrosSerializer, UsuariosSerializer
from django.shortcuts import get_object_or_404
from ..models import Usuarios, Livros
from rest_framework import viewsets

class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializer

class LivrosViewSet(viewsets.ModelViewSet):
    serializer_class = LivrosSerializer

    def get_queryset(self):
        idUsuario = self.request.session.get("usuario_id")
        if not idUsuario:
            return Livros.objects.none()
        return Livros.objects.filter(usuario_id=idUsuario).order_by("-data_aluguel", "-id")

    def perform_create(self, serializer):
        idUsuario = self.request.session.get("usuario_id")
        usuario = get_object_or_404(Usuarios, pk=idUsuario)
        serializer.save(usuario=usuario)
