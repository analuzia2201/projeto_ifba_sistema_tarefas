# Documentação do Modelo Lógico de Banco de Dados

**Projeto:** Sistema de Gerenciamento de Tarefas
**SGBD (Sistema de Gerenciamento de Banco de Dados):** SQLite3

## Entidades e Relacionamentos
O banco de dados é composto por duas entidades (tabelas) principais que se relacionam entre si na cardinalidade 1:N (Um para Muitos):
* Uma Categoria pode ter várias Tarefas vinculadas a ela.
* Uma Tarefa pertence a apenas uma Categoria.

[Link para o modelo lógico do banco de dados do sistema de tarefas](https://app.brmodeloweb.com/#!/publicview/69bb6aa7c7d1fc1a52ca18a9)

## Regras de Negócio (Constraints e Validações)
Embora algumas validações ocorram a nível de aplicação (Django), elas refletem a lógica do modelo de dados:
**1.	Data Limite:** *data_limite* não pode receber valores menores que a data atual do sistema (não permite datas no passado).
**2.	Data de Execução vs Limite:** Se *data_execucao* for preenchida, ela não pode ser posterior à *data_limite* e também não permite datas no passado.
**3.	Exclusão em Cascata:** O vínculo *models.CASCADE* garante a integridade referencial. Uma tarefa não pode existir sem uma categoria (não existem tarefas "órfãs").