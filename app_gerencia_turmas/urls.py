from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('cadastro_alunos/', views.cadastro_alunos, name='cadastro_alunos'),
    path('turma/<int:turma_id>/', views.turma_detalhe, name='turma_detalhe'),
    path('atividade/<int:atividade_id>/', views.atividade_detalhe, name='atividade_detalhe'),
    path('equipe/<int:equipe_id>/', views.equipe_detalhe, name='equipe_detalhe'),
    path('turma/<int:turma_id>/atividade/<int:atividade_id>/classificar/', views.classificar_atividade, name='classificar_atividade'),
]
