from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import RelatedFieldListFilter
from django.db.models import Q
from django import forms
from .models import Turma, Atividade, Equipe, Aluno, RealizacaoAtividade

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'data_criacao')
    list_fields = ('nome', 'descricao')
    list_filter = ('data_criacao',)

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display = ('nome','saldo_pontos', 'descricao', 'turma')
    list_fields =  ('nome', 'descricao', 'turma')
    list_filter = ('turma',)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'equipe', 'nome_da_turma', 'descricao_da_turma')
    list_fields = ('nome', 'equipe', 'nome_da_turma')
    list_filter = ('equipe',)

    def nome_da_turma(self, obj):
        return obj.equipe.turma.nome
    
    def descricao_da_turma(self, obj):
        return obj.equipe.turma.descricao

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'turma', 'pontos', 'data_entrega', 'data_criacao')
    list_fields = ('nome', 'turma', 'pontos', 'data_entrega')
    list_filter = ('turma', 'data_entrega')

class EquipeTurmaFilter(RelatedFieldListFilter):
    def field_choices(self, field, request, model_admin):
        # Obtém a turma selecionada no filtro de atividades
        turma_id = request.GET.get('atividade__turma__id')
        if turma_id:
            # Filtra as equipes pela turma selecionada
            return field.get_choices(
                include_blank=False,
                limit_choices_to=Q(turma__id=turma_id),
            )
        else:
            return field.get_choices(
                include_blank=False,
            )
        
class RealizacaoAtividadeForm(forms.ModelForm):
    equipe = forms.ModelChoiceField(queryset=None)

    def __init__(self, *args, **kwargs):
        atividade_id = kwargs.pop('atividade_id', None)
        super().__init__(*args, **kwargs)
        if atividade_id:
            atividade = Atividade.objects.get(id=atividade_id)
            self.fields['equipe'].queryset = atividade.turma.equipe_set.all()

    class Meta:
        model = RealizacaoAtividade
        fields = '__all__'

class RealizacaoAtividadeAdmin(admin.ModelAdmin):
    form = RealizacaoAtividadeForm
    list_display = ('atividade', 'equipe', 'realizada_com_sucesso')
    list_filter = ('atividade__turma', 'equipe', 'realizada_com_sucesso')
    search_fields = ('atividade__nome', 'equipe__nome')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def response_add(self, request, obj, post_url_continue=None):
        atividade_id = request.GET.get('atividade_id')
        if atividade_id:
            return self.response_post_save_change(request, obj)

        return super().response_add(request, obj, post_url_continue)

admin.site.register(RealizacaoAtividade, RealizacaoAtividadeAdmin)