# Generated migration for Activity model

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('prospect_added', 'Prospect Added'), ('client_added', 'Client Added'), ('status_updated', 'Status Updated'), ('meeting_scheduled', 'Meeting Scheduled'), ('other', 'Other')], max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='api.contact')),
                ('prospect', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='api.prospect')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'activities',
                'ordering': ['-timestamp'],
            },
        ),
    ]
