# Generated by Django 4.2.4 on 2023-09-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_word_delete_bottle"),
    ]

    operations = [
        migrations.AddField(
            model_name="webscraper",
            name="definition",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="webscraper",
            name="word",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="word",
            name="definition",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="word",
            name="word",
            field=models.TextField(default=""),
        ),
    ]
