# Generated by Django 4.0.4 on 2022-06-01 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_comment_comment_text_listing_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, max_length=500, verbose_name='Comment'),
        ),
    ]
