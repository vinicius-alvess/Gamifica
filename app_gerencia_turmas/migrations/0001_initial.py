# Generated by Django 4.2.2 on 2023-07-18 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('pontos', models.PositiveIntegerField()),
                ('data_entrega', models.DateField(blank=True)),
                ('descricao_detalhada', models.TextField(blank=True)),
                ('arquivos', models.FileField(blank=True, upload_to='media/')),
                ('recursos', models.URLField(blank=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Equipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('saldo_pontos', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RealizacaoAtividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realizada_com_sucesso', models.BooleanField(default=False)),
                ('atividade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_gerencia_turmas.atividade')),
                ('equipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_gerencia_turmas.equipe')),
            ],
        ),
        migrations.AddField(
            model_name='equipe',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_gerencia_turmas.turma'),
        ),
        migrations.AddField(
            model_name='atividade',
            name='turma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_gerencia_turmas.turma'),
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('equipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_gerencia_turmas.equipe')),
            ],
        ),
    ]