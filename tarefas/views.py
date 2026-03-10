from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
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
        return render(request, 'cadastrar_tarefa.html', {'categorias': lista_categorias})
    
    elif request.method == 'POST':
        titulo_digitado = request.POST.get('titulo')
        descricao_digitada = request.POST.get('descricao')
        data_entrega_digitada = request.POST.get('data_entrega')
        data_execucao_digitada = request.POST.get('data_execucao')

        id_categoria_escolhida = request.POST.get('categoria')
        categoria_escolhida = Categoria.objects.get(id=id_categoria_escolhida)

        nova_tarefa = Tarefa(
            nome = titulo_digitado,
            descricao = descricao_digitada,
            data_limite = data_entrega_digitada,
            data_execucao = data_execucao_digitada,
            categoria = categoria_escolhida
        )

        try:
            nova_tarefa.full_clean()
            nova_tarefa.save()
            messages.success(request, 'Tarefa cadastrada com sucesso!')

        except ValidationError as e:
            for mensagem_erro in e.messages:
                messages.error(request, f'Atenção: {mensagem_erro}')

        return redirect('/cadastrar_tarefa/')

def visualizar_tarefas(request):
    pass

def editar_tarefa(request):
    pass

def deletar_tarefa(request):
    pass

def deletar_categoria(request):
    pass