# Generated by Django 5.1.3 on 2025-03-01 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0004_alter_customuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type',
            field=models.CharField(choices=[('donor', 'Donor'), ('beneficiary', 'Beneficiary')], default=None, max_length=20),
        ),
    ]
