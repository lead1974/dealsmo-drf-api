# Generated by Django 5.0.2 on 2025-03-10 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0003_articlecategory_article_category"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="articlecategory",
            options={
                "ordering": ["sequence", "name"],
                "verbose_name": "Article Category",
                "verbose_name_plural": "Article Categories",
            },
        ),
        migrations.AddField(
            model_name="articlecategory",
            name="sequence",
            field=models.IntegerField(
                default=0, help_text="Order in which the category appears"
            ),
        ),
    ]
