from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
from .models import Tarefa, Categoria

def index(request):
    """entrega o arquivo HTML do menu"""
    return render(request, 'index.html')

def cadastrar_categoria(request):
    if request.method == 'POST':
        nome_digitado = request.POST.get('nome').strip()
        
        if Categoria.objects.filter(nome__iexact=nome_digitado).exists():
            messages.error(request, f'A categoria "{nome_digitado}" já está cadastrada!')

        else:
            Categoria.objects.create(nome=nome_digitado)
            messages.success(request, 'Categoria cadastrada com sucesso!')
        
        return redirect('/cadastrar_categoria/')
    
    return render(request, 'cadastrar_categoria.html')

def cadastrar_tarefa(request):
    if request.method == 'GET':
        lista_categorias = Categoria.objects.all()
        return render(request, 'cadastrar_tarefa.html', 
                      {'categorias': lista_categorias})
    
    elif request.method == 'POST':
        titulo_digitado = request.POST.get('titulo')
        descricao_digitada = request.POST.get('descricao')
        data_limite_digitada = request.POST.get('data_limite')
        horario_limite_digitado = request.POST.get('horario_limite')
        data_execucao_digitada = request.POST.get('data_execucao')

        id_categoria_escolhida = request.POST.get('categoria')
        categoria_escolhida = Categoria.objects.get(id=id_categoria_escolhida)

        if not data_execucao_digitada:
            data_execucao_digitada = None
        if not descricao_digitada:
            descricao_digitada = None

        nova_tarefa = Tarefa(
            nome = titulo_digitado,
            descricao = descricao_digitada,
            data_limite = data_limite_digitada,
            horario_limite = horario_limite_digitado,
            data_execucao = data_execucao_digitada,
            categoria = categoria_escolhida
        )

        try:
            nova_tarefa.full_clean()
            nova_tarefa.save()
            messages.success(request, 'Tarefa cadastrada com sucesso!')

            return redirect('/cadastrar_tarefa/')

        except ValidationError as e:
            for mensagem_erro in e.messages:
                messages.error(request, f'Atenção: {mensagem_erro}')

            lista_categorias = Categoria.objects.all()

            return render(request, 'cadastrar_tarefa.html', 
                          {'categorias': lista_categorias,
                           'dados': request.POST})
        
def minhas_tarefas(request):
    tempo_passado = timezone.now() - timedelta(hours=1)
    Tarefa.objects.filter(status='Concluída', data_conclusao__lt=tempo_passado).delete()

    lista_tarefas = Tarefa.objects.all()
    
    return render(request, 'minhas_tarefas.html', {'tarefas': lista_tarefas})

def alterar_status(request, id_tarefa):
    tarefa = Tarefa.objects.get(id=id_tarefa)

    if tarefa.status == 'Pendente':
        Tarefa.objects.filter(id=id_tarefa).update(status='Concluída', data_conclusao=timezone.now())

    else:
        Tarefa.objects.filter(id=id_tarefa).update(status='Pendente', data_conclusao=None)

    return redirect('/minhas_tarefas/')

def editar_tarefa(request):
    pass

def deletar_tarefa(request, id_tarefa):
    Tarefa.objects.filter(id=id_tarefa).delete()

    return redirect('/minhas_tarefas/')

def deletar_categoria(request):
    pass