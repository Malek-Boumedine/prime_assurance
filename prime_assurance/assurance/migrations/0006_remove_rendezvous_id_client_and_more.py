# Generated by Django 5.1.5 on 2025-01-28 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assurance', '0005_alter_user_sexe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rendezvous',
            name='id_client',
        ),
        migrations.RemoveField(
            model_name='rendezvous',
            name='id_operateur',
        ),
        migrations.AddField(
            model_name='rendezvous',
            name='nom',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='rendezvous',
            name='operateur',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='rendezvous',
            name='prenom',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='motif',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
