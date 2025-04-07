# Generated by Django 5.1.7 on 2025-04-07 18:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_assistant_assistantpermissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
                ('assistant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.assistant')),
            ],
        ),
        migrations.CreateModel(
            name='ConversationMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.JSONField()),
                ('date_of_creation', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.conversation')),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.usercredentials')),
            ],
        ),
        migrations.CreateModel(
            name='ConversationPermissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_edit', models.BooleanField(default=False)),
                ('can_delete', models.BooleanField(default=False)),
                ('can_view', models.BooleanField(default=False)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.conversation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.usercredentials')),
            ],
        ),
    ]
