# Generated by Django 3.0.6 on 2020-06-10 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multiphoto', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='multi',
            field=models.ForeignKey(default='non', on_delete=django.db.models.deletion.CASCADE, to='multiphoto.MultiPhoto'),
            preserve_default=False,
        ),
    ]