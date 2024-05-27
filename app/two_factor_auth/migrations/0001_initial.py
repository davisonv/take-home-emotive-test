# Generated by Django 4.2.3 on 2024-05-26 18:31

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AntiFraud',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('phone_number', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('last_status', models.CharField(choices=[('approved', 'approved'), ('unapproved', 'unapproved'), ('pending', 'pending')])),
                ('max_sequence_unapproved', models.IntegerField()),
            ],
        ),
    ]