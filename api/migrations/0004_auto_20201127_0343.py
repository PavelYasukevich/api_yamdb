# Generated by Django 3.0.5 on 2020-11-27 03:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201125_0419'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-year'], 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Необязательное к заполнению.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='api.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, help_text='Необязательное к заполнению.', related_name='titles', to='api.Genre', verbose_name='Жанр'),
        ),
    ]
