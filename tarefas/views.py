from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from .forms import TarefaForm, CategoriaForm
from .models import Tarefa, Categoria

def index(request):
    """entrega o arquivo HTML do menu"""
    return render(request, 'index.html')

def cadastrar_categoria(request):
    if request.method == 'POST': # pergunta se o usuário enviou
        form = CategoriaForm(request.POST) # preenche o formulário com tudo que o usuário digitou na tela
        
        if form.is_valid(): # verifica se os dados são válidos, de acordo com todas as restrições
            form.save() # salva os dados válidos
            messages.success(request, 'Categoria cadastrada com sucesso!')
        
            return redirect('/cadastrar_categoria/') # recarrega a página para cadastrar uma nova categoria
        
        else:
            for campo, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, f"{erro}")

    else: # Se o usuário não enviou nada ele acabou de chegar na página e é entregue um formulário vazio para ser preenchido
        form = CategoriaForm()

    return render(request, 'cadastrar_categoria.html', {'form': form}) # para poder aplicar o formulário no HTML

def cadastrar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarefa cadastrada com sucesso!')
            return redirect('/cadastrar_tarefa/')
        
        else:
            for campo, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, f"{erro}")

    else:
        form = TarefaForm()

    return render(request, 'cadastrar_tarefa.html', {'form': form})
        
def minhas_tarefas(request):
    """deleta as tarefas concluídas depois de 24hrs"""
    tempo_passado = timezone.now() - timedelta(hours=24) # define quando era 24hrs atrás
    Tarefa.objects.filter(status='Concluída', data_conclusao__lt=tempo_passado).delete() # deleta a tarefa que foi concluida e que tem data de conclusão menor que (mais antigo) que 24hrs atrás

    lista_tarefas = Tarefa.objects.all() # guarda as tarefas que sobraram
    
    return render(request, 'minhas_tarefas.html', {'tarefas': lista_tarefas}) # envia a lista para o HTML com o apelido tarefas

def alterar_status(request, id_tarefa):
    tarefa = Tarefa.objects.get(id=id_tarefa)

    if tarefa.status == 'Pendente':
        Tarefa.objects.filter(id=id_tarefa).update(status='Concluída', data_conclusao=timezone.now()) # muda o status de pendente para concluída e salva o momento que foi concluída

    else:
        Tarefa.objects.filter(id=id_tarefa).update(status='Pendente', data_conclusao=None) # muda o status de concluída para pendente e limpa a data que foi concluída

    return redirect('/minhas_tarefas/')

def editar_tarefa(request, id_tarefa):
    tarefa_editada = Tarefa.objects.get(id=id_tarefa)

    if request.method == 'GET': # vê os dados autuais da tarefa que clicou para editar
        form = TarefaForm(instance=tarefa_editada) # cria um formulário pré-preenchido com os dados que já estavam salvos no banco
        
    elif request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa_editada) # os novos dados são salvos, mas mantendo o vínculo com o objeto original sem cria um novo ID
        if form.is_valid(): # verifica se os novos dados são válidos
            form.save() # salva os novos dados válidos
            messages.success(request, 'Tarefa atualizada com sucesso!')
            return redirect('/minhas_tarefas/')
        
        else:
            for campo, erros in form.errors.items():
                for erro in erros:
                    messages.error(request, f"{erro}")

    return render(request, 'editar_tarefa.html', {'form': form, 'tarefa': tarefa_editada})

def deletar_tarefa(request, id_tarefa):
    Tarefa.objects.filter(id=id_tarefa).delete()

    return redirect('/minhas_tarefas/')

def visualizar_categoria(request):
    """Busca as categorias e desenha a página"""
    categorias_salvas = Categoria.objects.all()
    return render(request, 'deletar_categoria.html', {'categorias': categorias_salvas})

def confirmar_exclusao(request, id_categoria):
    categoria_alvo = Categoria.objects.get(id=id_categoria)
    
    tarefas_ameacadas = Tarefa.objects.filter(categoria=categoria_alvo) # busca no banco de dados todas as tarefas que pertencem a categoria selecionada

    if request.method == 'POST': # se confirmou a exclusão
        categoria_alvo.delete() # O CASCADE apaga as tarefas junto
        messages.success(request, f'Categoria "{categoria_alvo.nome}" e suas tarefas foram deletadas!')
        return redirect('/deletar_categoria/')

    return render(request, 'confirmar_exclusao.html', {'categoria': categoria_alvo, 'tarefas': tarefas_ameacadas})