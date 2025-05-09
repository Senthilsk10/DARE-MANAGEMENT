# Generated by Django 5.1 on 2025-04-10 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('projects', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('subject', models.TextField(default='Not Mentioned')),
                ('message_id', models.CharField(max_length=40)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.evaluator')),
            ],
        ),
        migrations.CreateModel(
            name='MailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Approach', 'Approach Email to viva coordinators'), ('Reminder', 'Reminder for pending mail'), ('Accepted', 'Mail received for acceptance of project'), ('Rejected', 'Mail received for project rejection'), ('Modifications', 'Mail about project modifications')], max_length=20)),
                ('object_id', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.TextField()),
                ('attachments', models.JSONField(default=list, help_text='Attachment URLs stored as JSON list')),
                ('subject', models.TextField(default='Not Mentioned')),
                ('message_id', models.CharField(max_length=40)),
                ('evaluator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.evaluator')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
