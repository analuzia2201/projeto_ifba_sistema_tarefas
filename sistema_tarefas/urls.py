from django.contrib import admin
from django.urls import path
import tarefas.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'), 
    path('cadastrar_tarefa/', views.cadastrar_tarefa, name='cadastrar_tarefa'),
    path('minhas_tarefas/', views.minhas_tarefas, name='minhas_tarefas'),
    path('alterar_status/<int:id_tarefa>/', views.alterar_status),
    path('deletar_tarefa/<int:id_tarefa>/', views.deletar_tarefa),
    path('editar_tarefa/', views.editar_tarefa, name='editar_tarefa'),
    path('deletar_categoria/', views.deletar_categoria, name='deletar_categoria'), 
]
