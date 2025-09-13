from django.db import models

class usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} - {self.email}"


class livros(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        usuarios,
        on_delete=models.CASCADE,
        db_column="usuario_id",   
        related_name="livros"
    )
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    data_aluguel = models.DateField(auto_now_add=True)  
    data_entrega = models.DateField()


    def __str__(self):
        return f"{self.titulo} - Alugado por {self.usuarios.nome} - data de aluguel: {self.data_aluguel} - data de entrega: {self.data_entrega}"

