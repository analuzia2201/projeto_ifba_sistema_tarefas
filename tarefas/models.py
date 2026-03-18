from django.db import models
from django.core.exceptions import ValidationError # Para o erro de data
from django.utils import timezone # Para saber que dia é hoje

def validar_data_limite(data):
    """Verifica se a data escolhida é válida"""
    if data < timezone.localtime().date(): # menor = mais antiga
        raise ValidationError('O prazo não pode ser no passado!')

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome
    
class Tarefa(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_limite = models.DateField(validators=[validar_data_limite])
    horario_limite = models.TimeField(default='23:59', null=True, blank=True) # opcional
    status = models.CharField(max_length=100, default='Pendente')
    data_execucao = models.DateField(null=True, blank=True, ) # opcional
    data_conclusao = models.DateTimeField(null=True, blank=True) # para poder deletar depois de 24hrs de concluída
    
    def clean(self):
        """Validação cruzada entre campos"""
        super().clean()

        hoje = timezone.localtime().date()
        agora = timezone.localtime().time()

        if self.data_execucao:
            if self.data_execucao < hoje:
                raise ValidationError({'data_execucao': 'A data de execução não pode ser no passado!'})

        if self.data_execucao and self.data_limite:
            if self.data_execucao > self.data_limite:
                raise ValidationError({'data_execucao': 'A data para executar a tarefa não pode ser posterior ao prazo!'})
            
        if self.data_limite and self.horario_limite:
            if self.data_limite == hoje:
                if self.horario_limite < agora:
                    raise ValidationError({'horario_limite': 'Atenção: Esse horário já passou!'})

    def save(self, *args, **kwargs):
        """Garante que a validação ocorra antes de salvar no banco"""
        self.full_clean() # obriga o Django a rodar todas as validações, incluindo a def clean()
        super().save(*args, **kwargs) # Salva no SQLit
    
    def __str__(self):
        return self.nome

    @property
    def cor_linha_tabela(self):
        hoje = timezone.localtime().date()

        if self.data_limite < hoje:
            return 'vermelho'
        
        elif self.data_execucao:
            if self.data_execucao < hoje:
                return 'laranja'
            
            elif self.data_execucao == hoje:
                return 'azul'
            
        return 'verde'