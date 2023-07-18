from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Turma, Equipe, Aluno, Atividade, RealizacaoAtividade
from random import sample
import pandas as pd
import os

def pagina_inicial(request):
    turmas = Turma.objects.all().order_by('-data_criacao')
    context = {'turmas': turmas}
    return render(request, 'app_gerencia_turmas/pagina_inicial.html', context)

def turmas(request):
    turmas = Turma.objects.all().order_by('-data_criacao')
    context = {'turmas': turmas}
    return render(request, 'app_gerencia_turmas/turmas.html', context)


def turma_detalhe(request, turma_id):
    turma = get_object_or_404(Turma, id=turma_id)
    atividades = Atividade.objects.filter(turma=turma).order_by('data_criacao')
    equipes = Equipe.objects.filter(turma=turma).order_by('-saldo_pontos')    
    context = {'turma': turma, 'atividades': atividades, 'equipes':equipes}
    return render(request, 'app_gerencia_turmas/turma_detalhe.html', context)

def atividade_detalhe(request, atividade_id):
    atividade = get_object_or_404(Atividade, id=atividade_id)
    
    # Obter as equipes que já realizaram a atividade com sucesso
    equipes_realizadas = Equipe.objects.filter(
        realizacaoatividade__atividade=atividade,
        realizacaoatividade__realizada_com_sucesso=True
    )
    
    # Obter todas as equipes da turma da atividade
    equipes = atividade.turma.equipe_set.all()
    
    context = {
        'atividade': atividade,
        'equipes_realizadas': equipes_realizadas,
        'equipes': equipes
    }
    return render(request, 'app_gerencia_turmas/atividade_detalhe.html', context)


def equipe_detalhe(request, equipe_id):
    equipe = get_object_or_404(Equipe, id=equipe_id)
    context = {'equipe': equipe}
    return render(request, 'app_gerencia_turmas/equipe_detalhe.html', context)

def cadastro_alunos(request):
    turmas = Turma.objects.all()

    if request.method == 'POST':
        arquivo = request.FILES['arquivo']
        turma_id = request.POST.get('turma')
        quantidade_equipes = int(request.POST.get('equipes'))

         # Obter a extensão do arquivo
        _, ext = os.path.splitext(arquivo.name)

        if ext.lower() in ['.xlsx', '.xls', '.xlsm']:
            df = pd.read_excel(arquivo)
            alunos = list(df.to_dict('records'))
            random_alunos = sample(alunos, len(alunos))  # Embaralhar a ordem dos alunos

            try:
                turma = Turma.objects.get(id=turma_id)
                equipes_criadas = []

                # Criar as equipes
                for i in range(1, quantidade_equipes + 1):
                    equipe = Equipe.objects.create(nome=f'Equipe {i}', turma=turma)
                    equipes_criadas.append(equipe)

                # Distribuir os alunos nas equipes
                num_equipes = len(equipes_criadas)
                equipe_index = 0

                for aluno in random_alunos:
                    matricula = aluno['Matricula']
                    email = aluno['Email']
                    username = matricula

                    # Verificar se o usuário já existe
                    try:
                        user = User.objects.get(username=username)
                        # Se o usuário já existe, atualizar as informações
                        user.email = email
                        user.save()
                    except User.DoesNotExist:
                        # Se o usuário não existe, criar um novo usuário
                        password = User.objects.make_random_password()
                        user = User.objects.create_user(username=username, password=password, email=email)

                    # Associar o aluno à equipe
                    equipe_atual = equipes_criadas[equipe_index]
                    aluno = Aluno.objects.create(nome=username, equipe=equipe_atual)
                    equipe_atual.aluno_set.add(aluno)
                    equipe_atual.save()

                    equipe_index = (equipe_index + 1) % num_equipes

                messages.success(request, 'Usuários criados e distribuídos com sucesso!')
            except Turma.DoesNotExist:
                messages.warning(request, f'Turma {turma_id} não encontrada.')
        else:
            messages.error(request, 'Arquivo inválido. Por favor, selecione um arquivo .xlsx.')

    context = {'turmas': turmas}
    return render(request, 'app_gerencia_turmas/cadastro_alunos.html', context)

from django.contrib import messages

def classificar_atividade(request, turma_id, atividade_id):
    turma = get_object_or_404(Turma, id=turma_id)
    atividade = get_object_or_404(Atividade, id=atividade_id)
    equipes = Equipe.objects.filter(turma=turma)

    if request.method == 'POST':
        equipes_selecionadas = request.POST.getlist('equipes')
        for equipe_id in equipes_selecionadas:
            equipe = get_object_or_404(Equipe, id=equipe_id)
            # Verificar se a equipe já realizou a atividade com sucesso
            if RealizacaoAtividade.objects.filter(equipe=equipe, atividade=atividade, realizada_com_sucesso=True).exists():
                messages.error(request, f"A equipe {equipe.nome} já realizou a atividade com sucesso.")
                continue

            realizacao_atividade = RealizacaoAtividade.objects.create(equipe=equipe, atividade=atividade, realizada_com_sucesso=True)
            # Atualizar saldo de pontos da equipe
            equipe.saldo_pontos += atividade.pontos
            equipe.save()

        return redirect('atividade_detalhe', atividade_id=atividade.id)

    context = {
        'turma': turma,
        'atividade': atividade,
        'equipes': equipes,
    }
    return render(request, 'app_gerencia_turmas/classificar_atividade.html', context)

