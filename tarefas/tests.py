from django.test import TestCase
from django.utils import timezone
from .models import Categoria, Tarefa
from datetime import timedelta

class TarefaModelTest(TestCase):

    def setUp(self):
        """é executado antes de cada teste da classe"""
        self.categoria = Categoria.objects.create(nome="Estudos") # Cria dados iniciais para os testes

    def test_criacao_tarefa_sucesso(self):
        """testa se uma tarefa é criada corretamente no banco"""
        tarefa = Tarefa.objects.create(
            nome = "Estudar Django",
            data_limite = timezone.now().date() + timedelta(days=1),
            categoria = self.categoria
        ) # cria e salva uma tarefa no banco de dados temporário de testes
        self.assertEqual(tarefa.nome, "Estudar Django") # faz o teste
        self.assertEqual(tarefa.status, 'Pendente')

    def test_pagina_lista_tarefas_carrega(self):
        """testa se a página de listagem retorna status 200 (OK)"""
        response = self.client.get('/minhas_tarefas/') # guarda tudo o que o servidor devolve ao acessar a página minhas tarefas
        self.assertEqual(response.status_code, 200) # verifica se está tudo ok (status 200)

    def test_validacao_data_passada(self):
        """testa se o sistema permite salvar data no passado (deve falhar)"""
        tarefa_errada = Tarefa(
            nome = "Tarefa do passado",
            data_limite = timezone.now().date() - timedelta(days=5), # a tarefa é criada com prazo de entrega para a semana passada
            categoria = self.categoria
        ) # o objeto é montado na memória do computador, mas ainda não é salvo no banco de dados
        
        with self.assertRaises(Exception): # verifica se vai dar erro (que é o esperado)
            tarefa_errada.full_clean() # pega o objeto da memória e verifica de acordo com todas as regras de validação que ta no models.py

    def test_cadastrar_tarefa_via_formulario(self):
        """Testa se o envio do formulário (POST) realmente cria a tarefa"""
        dados_do_formulario = {
            'nome': 'Comprar pão',
            'data_limite': timezone.now().date() + timedelta(days=2),
            'categoria': self.categoria.id
        } # prepara os dados como se fossem digitados no formulário HTML
        
        response = self.client.post('/cadastrar_tarefa/', dados_do_formulario) # o navegador fantasma "clica em salvar" enviando os dados
        
        self.assertEqual(response.status_code, 302) # verifica se cumpriu o ciclo completo de salvar o dado e limpar a tela redirecionando a navegação
        self.assertTrue(Tarefa.objects.filter(nome='Comprar pão').exists()) # verifica se o dado realmente foi parar no banco de dados