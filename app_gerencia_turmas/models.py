from django.db import models
from django.db.models import Sum

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Equipe(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    saldo_pontos = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nome
    
    def realizou_atividade_com_sucesso(self, atividade):
        return RealizacaoAtividade.objects.filter(equipe=self, atividade=atividade, realizada_com_sucesso=True).exists()
    
    def save(self, *args, **kwargs):
        # Calcula o saldo de pontos com base nas realizações de atividades
        self.saldo_pontos = RealizacaoAtividade.objects.filter(equipe=self, realizada_com_sucesso=True).aggregate(Sum('atividade__pontos'))['atividade__pontos__sum'] or 0
        super().save(*args, **kwargs)

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Atividade(models.Model):
    nome = models.CharField(max_length=100)
    pontos = models.PositiveIntegerField()
    data_entrega = models.DateField(blank=True)
    descricao_detalhada = models.TextField(blank=True)
    arquivos = models.FileField(upload_to='media/', blank=True)
    recursos = models.URLField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class RealizacaoAtividade(models.Model):
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    realizada_com_sucesso = models.BooleanField(default=False)

    def __str__(self):
        return f'Realização da atividade {self.atividade} pela equipe {self.equipe}'
