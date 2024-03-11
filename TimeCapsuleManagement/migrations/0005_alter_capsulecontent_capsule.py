# Generated by Django 5.0.1 on 2024-03-10 15:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeCapsuleManagement', '0004_alter_capsulecontent_capsule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capsulecontent',
            name='capsule',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='media', to='TimeCapsuleManagement.capsule'),
            preserve_default=False,
        ),
    ]
