from django import forms

class UsuariosForm(forms.Form):
    nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Seu nome"})
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "seuemail@exemplo.com"})
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "placeholder": "Crie uma senha"})
    )

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))
    
