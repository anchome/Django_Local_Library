# Generated by Django 4.1.7 on 2023-03-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_language_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='born'),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='died'),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text='Introduzca el idioma natural del libro (por ejemplo, inglés, francés, japonés, etc.)".', max_length=50),
        ),
    ]
