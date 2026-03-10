from django.db import models
from django.core.exceptions import ValidationError # Para o erro de data
from django.utils import timezone # Para saber que dia é hoje

def validar_data_limite(data):
    """Verifica se a data escolhida é válida"""
    if data < timezone.now().date():
        raise ValidationError('A data limite não pode ser no passado!')

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

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
    
    def clean(self):
        """Validação cruzada entre campos"""
        super().clean()
        
        if self.data_execucao and self.data_limite:
            if self.data_execucao > self.data_limite:
                raise ValidationError({'data_execucao': 'A data para executar a tarefa não pode ser posterior ao prazo!'})

    def save(self, *args, **kwargs):
        """Garante que a validação ocorra antes de salvar no banco"""
        self.full_clean()
        super().save(*args, **kwargs) # Salva no SQLit
    
    def __str__(self):
        return self.nome

