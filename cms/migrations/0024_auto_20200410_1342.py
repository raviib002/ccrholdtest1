# Generated by Django 2.2.11 on 2020-04-10 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0023_auto_20200410_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='publisher_public',
            field=models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publisher_draft', to='cms.Page'),
        ),
    ]