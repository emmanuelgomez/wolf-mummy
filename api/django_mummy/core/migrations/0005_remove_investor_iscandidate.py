# Generated by Django 2.0.2 on 2019-03-06 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_investor_iscandidate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investor',
            name='isCandidate',
        ),
    ]
