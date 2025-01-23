# Generated by Django 5.1.5 on 2025-01-23 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assurance', '0008_rename_status_fumeur_user_statut_fumeur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='region',
            field=models.CharField(blank=True, choices=[('northest', 'Northest'), ('northeast', 'Northeast'), ('southest', 'Southest'), ('southeast', 'Southeast')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sexe',
            field=models.CharField(blank=True, choices=[('male', 'Homme'), ('female', 'Femme')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='statut_fumeur',
            field=models.CharField(blank=True, choices=[('yes', 'Oui'), ('no', 'Non')], max_length=3, null=True),
        ),
    ]
