# Generated by Django 3.2 on 2023-05-24 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0006_alter_honoraryteachers_name'),
        ('curriculum', '0004_auto_20230523_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='new_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_new', to='app_users.news'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='lesson_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_lesson', to='curriculum.lesson'),
        ),
    ]
