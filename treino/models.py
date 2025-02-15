from django.db import models

class Alunos(models.Model):

    faixa_choices = (
        ('B', 'Branca'),
        ('A', 'Azul'),
        ('R', 'Roxa'),
        ('M', 'Marrom'),
        ('P', 'Preta')
    )

    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    faixa = models.CharField(max_length=1, choices=faixa_choices, default='B')

    def __str__(self):
        return self.nome
