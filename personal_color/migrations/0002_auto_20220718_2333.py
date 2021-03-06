# Generated by Django 3.2.7 on 2022-07-18 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal_color', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colors',
            name='base_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='co_base', to='personal_color.base_type', verbose_name='ベースタイプ'),
        ),
        migrations.AlterField(
            model_name='items',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itm_color', to='personal_color.colors', verbose_name='色名'),
        ),
    ]
