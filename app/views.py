from django.contrib.auth.hashers import check_password
from django.views.generic import FormView
from django.shortcuts import render
from django.contrib import messages
from .forms import *
from django.urls import reverse_lazy
import requests

from .forms import UsuariosForm

from app.api.serializers import UsuariosSerializer


def listaDeLivros(request):
    q = request.GET.get("q", "populares")
    page = request.GET.get("page", 1)

    res = requests.get("https://openlibrary.org/search.json", params={"q": q, "page": page})
    data = res.json()

    livros = [
        {
            "titulo": d.get("title", "Sem título"),
            "autor": (d.get("author_name") or ["Desconhecido"])[0],
            "ano": d.get("first_publish_year", "—"),
            "capa_id": d.get("cover_i"),
            "key": d.get("key"),
        }
        for d in data.get("docs", [])[:20]
    ]

    return render(request, "home.html", {"q": q, "livros": livros})


class cadastroUsuario(FormView):
    template_name = "cadastro.html"
    form_class = UsuariosForm                         
    success_url = reverse_lazy("home")                

    def form_valid(self, form):
        # Passa os dados validados do Form para o DRF Serializer
        serializer = UsuariosSerializer(data=form.cleaned_data)  
        if serializer.is_valid():
            serializer.save()   #
            messages.success(self.request, "Usuário cadastrado com sucesso!")
            return super().form_valid(form)

        # Repassa erros do serializer para o form (exibidos no template)
        for field, msgs in serializer.errors.items():
            for msg in msgs:
                if field in form.fields:
                    form.add_error(field, msg)
                else:
                    form.add_error(None, msg)
        return self.form_invalid(form)


           

    
        
