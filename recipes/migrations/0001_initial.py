# Generated by Django 4.1.6 on 2023-03-24 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tag', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=65)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=65, verbose_name='Title')),
                ('description', models.CharField(max_length=165, verbose_name='Description')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('prep_time', models.IntegerField(verbose_name='Prep Time')),
                ('prep_time_unit', models.CharField(max_length=65, verbose_name='Prep Time Unit')),
                ('servings', models.IntegerField(verbose_name='Servings')),
                ('servings_unit', models.CharField(max_length=65, verbose_name='Servings Unit')),
                ('prep_steps', models.TextField(verbose_name='Prep Steps')),
                ('prep_steps_is_html', models.BooleanField(default=False, verbose_name='Prep Steps is HTML')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
                ('cover', models.ImageField(blank=True, default='', upload_to='recipes/covers/%Y/%m/%d/', verbose_name='Cover')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='recipes.category', verbose_name='Category')),
                ('tags', models.ManyToManyField(blank=True, default='', to='tag.tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes',
            },
        ),
    ]
