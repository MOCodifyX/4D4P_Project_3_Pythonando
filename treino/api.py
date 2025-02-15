from ninja import Router

treino_router = Router()

@treino_router.get('')
def criar_aluno(request):
    return {'Ola mundo!': 'Ola mundo!'}