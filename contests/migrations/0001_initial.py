# Generated by Django 4.1.7 on 2023-07-03 04:17

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration_minutes', models.IntegerField()),
                ('contest_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('problem_statement', ckeditor.fields.RichTextField()),
                ('code', models.CharField(max_length=255)),
                ('input_statement', ckeditor.fields.RichTextField()),
                ('constraint_statement', ckeditor.fields.RichTextField()),
                ('output_statement', ckeditor.fields.RichTextField()),
                ('editorial', ckeditor.fields.RichTextField(default='Coming Soon')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.contest')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Testcases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_file', models.FileField(default=None, upload_to='C:\\Users\\harsh\\Desktop\\oj\\oj/static')),
                ('answer_file', models.FileField(default=None, upload_to='C:\\Users\\harsh\\Desktop\\oj\\oj/static')),
                ('is_sample_testcase', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.question')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('language', models.CharField(max_length=50)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('verdict', models.CharField(max_length=50)),
                ('submitted_code', models.CharField(max_length=255)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
