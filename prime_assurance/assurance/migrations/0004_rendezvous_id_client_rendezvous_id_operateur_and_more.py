# Generated by Django 5.1.5 on 2025-01-23 12:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assurance', '0003_alter_user_sexe_alter_user_statut_fumeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendezvous',
            name='id_client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rdv_client', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rendezvous',
            name='id_operateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rdv_operateur', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='charges',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='nombre_enfants',
            field=models.IntegerField(null=True),
        ),
    ]
