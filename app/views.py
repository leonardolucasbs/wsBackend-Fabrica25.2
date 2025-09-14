from django.shortcuts import render, redirect, get_object_or_404                
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator        
from django.views.generic import FormView              
from django.urls import reverse_lazy                    
from django.contrib import messages                     
from django.shortcuts import redirect
from app.models import Usuarios, Livros
from datetime import date                    
from .forms import *
import requests

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
        
        serializer = UsuariosSerializer(data=form.cleaned_data)  
        if serializer.is_valid():
            serializer.save()   
            messages.success(self.request, "Usuário cadastrado com sucesso!")
            return super().form_valid(form)
        
       
        for field, msgs in serializer.errors.items():
            for msg in msgs:
                if field in form.fields:
                    form.add_error(field, msg)
                else:
                    form.add_error(None, msg)
        return self.form_invalid(form)

class loginUsuario(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        senha = form.cleaned_data["senha"]

        try:
            usuario = Usuarios.objects.get(email__iexact=email)
        except Usuarios.DoesNotExist:
            form.add_error("email", "E-mail não encontrado.")
            return self.form_invalid(form)

        if not check_password(senha, usuario.senha):
            form.add_error("senha", "Senha incorreta.")
            return self.form_invalid(form)

        # Marca login e faz a sessão expirar ao fechar o navegador
        self.request.session["usuario_id"] = usuario.id
        self.request.session.set_expiry(0)   # <- expira ao fechar o browser
        return super().form_valid(form) 

def alugarLivro(request):
    
    idUsuario = request.session.get("usuario_id")
    if not idUsuario:
        return redirect("loginUsuario")

    if request.method == "GET":
        
        titulo  = (request.GET.get("titulo") or "").strip()
        autor   = (request.GET.get("autor") or "").strip()
        capa_id_raw = request.GET.get("capa_id")
        capa_id = int(capa_id_raw) if (capa_id_raw and capa_id_raw.isdigit()) else None
        ano     = request.GET.get("ano") or ""
        key     = request.GET.get("key") or ""

        form = AlugarForm(initial={"titulo": titulo, "autor": autor})
        ctx = {
            "titulo": titulo,
            "autor": autor,
            "capa_id": capa_id,
            "ano": ano,
            "key": key,
            "form": form,
            "today": date.today().isoformat(),  
        }
        return render(request, "aluguel.html", ctx)

    
    form = AlugarForm(request.POST)
    if not form.is_valid():
        
        ctx = {
            "titulo": request.POST.get("titulo", ""),
            "autor": request.POST.get("autor", ""),
            "capa_id": request.POST.get("capa_id"),
            "ano": request.POST.get("ano"),
            "key": request.POST.get("key"),
            "form": form,
            "today": date.today().isoformat(),
        }
        return render(request, "aluguel.html", ctx)

    usuario = get_object_or_404(Usuarios, pk=idUsuario)
    Livros.objects.create(usuario=usuario, **form.cleaned_data)
    return redirect("home")

@never_cache
def locacoes(request):
    idUsuario = request.session.get("usuario_id")
    if not idUsuario:
        return redirect("loginUsuario")

    usuario = get_object_or_404(Usuarios, pk=idUsuario)
    livros = usuario.livros.all().order_by("-data_aluguel", "-id")
    return render(request, "locacoes.html", {"usuario": usuario, "livros": livros})
    
def logout(request):
    request.session.flush()  
    return redirect("loginUsuario")

       
