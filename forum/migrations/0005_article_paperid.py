# Generated by Django 2.2.5 on 2019-10-26 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20190809_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='paperId',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
