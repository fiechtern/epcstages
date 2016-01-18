# Generated by Django 1.9.1 on 2016-01-18 12:23
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stages', '0005_extended_contact_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporation',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                to='stages.Corporation', verbose_name='Institution mère'),
        ),
    ]
