# Generated by Django 5.1.4 on 2024-12-15 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_content_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='pub_date',
            new_name='created_at',
        ),
    ]
