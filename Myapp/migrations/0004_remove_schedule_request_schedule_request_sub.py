# Generated by Django 4.0.1 on 2023-10-10 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0003_category_coins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='REQUEST',
        ),
        migrations.AddField(
            model_name='schedule',
            name='REQUEST_SUB',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Myapp.request_sub'),
        ),
    ]