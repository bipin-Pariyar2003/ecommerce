# Generated by Django 5.0.6 on 2024-06-10 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0011_remove_user_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project_app.category'),
            preserve_default=False,
        ),
    ]