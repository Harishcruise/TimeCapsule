# Generated by Django 4.2.11 on 2024-03-23 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeCapsuleManagement', '0006_alter_capsule_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='capsule',
            old_name='status',
            new_name='is_published',
        ),
    ]
