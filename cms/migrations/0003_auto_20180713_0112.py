# Generated by Django 2.0.6 on 2018-07-12 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20180713_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pid',
            field=models.ForeignKey(default='null', null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Comment'),
        ),
    ]