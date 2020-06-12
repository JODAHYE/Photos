# Generated by Django 3.0.6 on 2020-06-12 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('multiphoto', '0004_multicomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='multiphoto',
            name='tags',
            field=models.ManyToManyField(to='multiphoto.Tag'),
        ),
    ]
