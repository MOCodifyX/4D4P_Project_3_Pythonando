from ninja import Router
from .schemas import AlunosSchema
from .models import Alunos
from ninja.errors import HttpError
from typing import List

treino_router = Router()

@treino_router.post('', response={200: AlunosSchema})
def criar_aluno(request, aluno_schema: AlunosSchema):
    nome = aluno_schema.dict()['nome']
    email = aluno_schema.dict()['email']
    faixa = aluno_schema.dict()['faixa']
    data_nascimento = aluno_schema.dict()['data_nascimento']

    if Alunos.objects.filter(email=email).exists():
        raise HttpError(400, "E-mail já cadastrado.")

    aluno = Alunos(nome=nome,
                    email=email, 
                    faixa=faixa,
                    data_nascimento=data_nascimento)
    aluno.save()

    return aluno

@treino_router.get('/alunos/', response=List[AlunosSchema])
def listar_alunos(request):
    alunos = Alunos.objects.all()
    return alunos