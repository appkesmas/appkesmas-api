# Generated by Django 3.2.3 on 2021-06-07 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_article'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='article',
            new_name='content',
        ),
        migrations.AddField(
            model_name='article',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
