# Generated by Django 5.0.3 on 2024-03-10 15:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeCapsuleManagement', '0003_alter_subscription_capsule_capsulecontent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capsulecontent',
            name='capsule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media', to='TimeCapsuleManagement.capsule'),
        ),
    ]