# Generated by Django 4.1.6 on 2023-02-18 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_alter_category_options_alter_recipe_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=65),
        ),
    ]
