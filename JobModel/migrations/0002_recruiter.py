# Generated by Django 3.1 on 2020-08-15 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobModel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='recruiter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=300)),
                ('describe', models.CharField(max_length=500)),
                ('user_type', models.CharField(max_length=100)),
            ],
        ),
    ]
