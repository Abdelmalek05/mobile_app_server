# Migration to populate user field and make it non-nullable

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion
from django.contrib.auth.models import User


def populate_user(apps, schema_editor):
    """Assign all contacts and prospects to the first available user, or a system user"""
    Contact = apps.get_model('api', 'Contact')
    Prospect = apps.get_model('api', 'Prospect')
    
    # Get or create a system user for orphaned records
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(username='system', is_active=False)
    
    # Update all contacts without a user
    Contact.objects.filter(user__isnull=True).update(user=user)
    
    # Update all prospects without a user
    Prospect.objects.filter(user__isnull=True).update(user=user)


def reverse_populate(apps, schema_editor):
    """Reverse: set user back to NULL (optional)"""
    Contact = apps.get_model('api', 'Contact')
    Prospect = apps.get_model('api', 'Prospect')
    Contact.objects.all().update(user=None)
    Prospect.objects.all().update(user=None)


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_add_user_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(populate_user, reverse_populate),
        migrations.AlterField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prospect',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prospects', to=settings.AUTH_USER_MODEL),
        ),
    ]
