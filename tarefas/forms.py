from django import forms # gera HTML e valida dados
from .models import Tarefa, Categoria

class CategoriaForm(forms.ModelForm):
    """cria um formulário HTML baseado em na tabela Categoria criada no models.py"""
    class Meta:
        model = Categoria # o formulário vai salvar os dados na tabela Categoria
        fields = ['nome']
        
        widgets = {'nome': forms.TextInput(attrs={'placeholder': 'Ex: Estudos, Casa, Trabalho...'})}
        
        labels = {'nome': 'Nome da Nova Categoria:'}

        error_messages = {'nome': {'unique': 'Esta categoria já existe!'}} # impede de criar categorias com o nome repetido

    def clean_nome(self): # o método clean_: executa antes de salvar no banco
        nome = self.cleaned_data.get('nome') # limpa o dado

        # __iexact busca no banco ignorando maiúsculas e minúsculas
        # exclude procura categorias com esse nome, mas ignore a própria categoria que está sendo editada
        if Categoria.objects.filter(nome__iexact=nome).exclude(id=self.instance.id).exists(): 
            raise forms.ValidationError('Esta categoria já existe!') # cancela o salvamento no banco de dados

        return nome

class TarefaForm(forms.ModelForm):
    """cria um formulário HTML baseado em na tabela Tarefa criada no models.py"""
    class Meta:
        model = Tarefa # o formulário vai salvar os dados na tabela Tarefa
        fields = ['nome', 'descricao', 'categoria', 'data_limite', 'horario_limite', 'data_execucao']
        
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Ex: Estudar para a prova'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Detalhes da Tarefa...'}),
            'data_limite': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'horario_limite': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'value': '23:59'}),
            'data_execucao': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),}
    
        labels = {
            'nome': 'Título da Tarefa:',
            'descricao': 'Descrição (Opcional):',
            'categoria': 'Categoria:',
            'data_limite': 'Prazo:',
            'horario_limite': 'Horário Limite:',
            'data_execucao': 'Quando deseja começar a fazer a tarefa? (Opcional)'}