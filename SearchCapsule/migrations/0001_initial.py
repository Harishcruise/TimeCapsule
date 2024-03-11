# Generated by Django 5.0.1 on 2024-03-11 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TimeCapsuleManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchableCapsule',
            fields=[
                ('capsule', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='TimeCapsuleManagement.capsule')),
            ],
        ),
    ]
