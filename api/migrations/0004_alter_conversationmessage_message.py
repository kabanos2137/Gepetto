# Generated by Django 5.1.7 on 2025-04-07 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_conversation_conversationmessage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversationmessage',
            name='message',
            field=models.TextField(),
        ),
    ]
