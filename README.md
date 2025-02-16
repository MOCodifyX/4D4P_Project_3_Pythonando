# 🚀Evento 4 Days 4 Projects da Pythonando🚀

---

## 📌 Projeto 3 - Rest API - Back-Emd

BACK-END de uma aplicação para academias de Jiu Jitsu organizarem seus alunos.💻

---

🔹Para iniciar o projeto, execute os seguintes comandos:

	python manage.py runserver


	acesso o link : http://127.0.0.1:8000/api/docs#/
 
---

## 🎓 Sistema de Gestão de Alunos

![image](https://github.com/user-attachments/assets/bf595f64-3da0-4531-9592-63c5b227826e)

- 📝 Cadastro de Alunos
  
> Permite o registro de novos alunos no sistema.
> ![image](https://github.com/user-attachments/assets/0f744d12-cc58-4c33-82d7-ec1a1ecbe61c)

- 📋 Lista de Alunos

> Lista todos os alunos cadastrados no sistema.
> ![image](https://github.com/user-attachments/assets/48ddbaf5-7ad8-4fe4-97d3-1211ef1f948e)

- 🏅 Progressão do Aluno
  
> Mostra o progresso do aluno para a próxima faixa.
> ![image](https://github.com/user-attachments/assets/9be21b18-8623-4161-9017-4412090a4c7f)

- 📚 Aulas Realizadas

> Interface para registrar as aulas realizadas de cada aluno.
> ![image](https://github.com/user-attachments/assets/fa6f993e-dc97-4bd5-93bc-ee87ce4912a6)

- ✏️ Atualização de Dados

> Interface para atualizar os dados cadastrais dos alunos.
> ![image](https://github.com/user-attachments/assets/56f80add-3a89-4a9f-9924-93cd153101f8)

---

# 🔧 Material de Apoio disponibilizado pelo Instrutor

> ### 🚨 Em caso de dúvidas, compare com o código do repositório para possíveis correções. O material de apoio é apenas uma base para montar o projeto!

---

## Passos iniciais

Primeiro devemos criar o ambiente virtual:

```python
# Criar
	# Linux
		python3 -m venv venv
	# Windows
		python -m venv venv
```

Após a criação do venv vamos ativa-lo:

```python
#Ativar
	# Linux
		source venv/bin/activate
	# Windows
		venv\Scripts\Activate

# Caso algum comando retorne um erro de permissão execute o código e tente novamente:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Agora vamos fazer a instalação do Django e as demais bibliotecas:

```python
pip install django
pip install pillow
pip install django-ninja
```

Vamos criar o nosso projeto Django:

```jsx
django-admin startproject core .
```

Rode o servidor para testar:

```jsx
python manage.py runserver
```

Crie o app usuario:

```jsx
python manage.py startapp treino
```

Ative o auto-save

INSTALE O APP!

Crie uma URL para API:

```python
from .api import api

path('api/', api.urls)
```

Crie um router para api em core/api.py:

```python
from ninja import NinjaAPI
from treino.api import treino_router

api = NinjaAPI()
api.add_router('', treino_router)
```

## Alunos

Primeiro passo, crie a model para armazenar os alunos:

```python
faixa_choices = (
        ('B', 'Branca'),
        ('A', 'Azul'),
        ('R', 'Roxa'),
        ('M', 'Marrom'),
        ('P', 'Preta')
    )

class Alunos(models.Model):
    
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    faixa = models.CharField(max_length=1, choices=faixa_choices, default='B')
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome
```

Crie o SCHEMA da model:

```python
from ninja import ModelSchema
from .models import Alunos

class AlunosSchema(ModelSchema):
    class Meta:
        model = Alunos
        fields = ['nome', 'email', 'faixa', 'data_nascimento']
```

Desenvolva um endpoint para criar o aluno:

```python
from ninja import Router
from ninja.errors import HttpError
from .schemas import AlunosSchema
from .models import Alunos

treino_router = Router()

@treino_router.post('/', response={200: AlunosSchema})
def criar_aluno(request, aluno_schema: AlunosSchema):
    nome = aluno_schema.dict()['nome']
    email = aluno_schema.dict()['email']
    faixa = aluno_schema.dict()['faixa']
    data_nascimento = aluno_schema.dict()['data_nascimento']

    if Alunos.objects.filter(email=email).exists():
        raise HttpError(400, "E-mail já cadastrado.")

    aluno = Alunos(nome=nome, email=email, faixa=faixa, data_nascimento=data_nascimento)
    aluno.save()
    
    return aluno

```

E o endpoint para listar todos os alunos:

```python
@treino_router.get('/alunos/', response=List[AlunosSchema])
def listar_alunos(request):
    alunos = Alunos.objects.all()
    return alunos
```

## Aulas

Aqui, vamos criar uma tabela para armazenar as aulas realizadas por um aluno:

```python
class AulasConcluidas(models.Model):
    aluno = models.ForeignKey(Alunos, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    faixa_atual = models.CharField(max_length=1, choices=faixa_choices)

    def __str__(self):
        return self.aluno.nome
```

Crie a função responsável pelo nível de progressão das faixas:

```python
import math

order_belt = {'Branca': 0, 'Azul': 1, 'Roxa': 2, 'Marrom': 3, 'Preta': 4 }

def calculate_lessons_to_upgrade(n):
    d = 1.47
    k = 30 / math.log(d)

    aulas = k * math.log(n + d)
    
    return round(aulas)
```

Crie o Schema:

```python
class ProgressoAlunoSchema(Schema):
    email: str
    nome: str
    faixa: str
    total_aulas: int
    aulas_necessarias_para_proxima_faixa: int

```

Construa a VIEW:

```python
@treino_router.get('/progresso_aluno/', response={200: ProgressoAlunoSchema})
def progresso_aluno(request, email_aluno: str):
    aluno = Alunos.objects.get(email=email_aluno)
    
    total_aulas_concluidas = AulasConcluidas.objects.filter(aluno=aluno).count()
    
    faixa_atual = aluno.get_faixa_display()
    
    n = order_belt.get(faixa_atual, 0)
  
    total_aulas_proxima_faixa = calcula_aulas_necessarios_proximo_nivel(n)

    total_aulas_concluidas_faixa = AulasConcluidas.objects.filter(aluno=aluno, faixa_atual=aluno.faixa).count()

    aulas_faltantes = max(total_aulas_proxima_faixa - total_aulas_concluidas_faixa, 0)

    
```

E para finalizar o projeto, desenvolva a funcionalidade para atualizar os dados de um aluno:

```python
@treino_router.put("/alunos/{aluno_id}", response=AlunosSchema)
def update_aluno(request, aluno_id: int, aluno_data: AlunosSchema):
    aluno = get_object_or_404(Alunos, id=aluno_id)
    
    idade = date.today() - aluno.data_nascimento

    if int(idade.days/365) < 18 and aluno_data.dict()['faixa'] in ('A', 'R', 'M', 'P'):
        raise HttpError(400, "O aluno é menor de idade e não pode ser graduado para essa faixa.")

    #exclude_unset=True
    for attr, value in aluno_data.dict().items():
        if value:
            setattr(aluno, attr, value)
    
    aluno.save()
    return aluno
```
