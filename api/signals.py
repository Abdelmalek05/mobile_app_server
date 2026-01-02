from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Contact, Prospect, Activity


def get_system_user():
    """Get or create the system user for tracking activities"""
    user, _ = User.objects.get_or_create(username='system', defaults={'is_active': False})
    return user


@receiver(post_save, sender=Contact)
def track_contact_activity(sender, instance, created, **kwargs):
    """
    Track Contact CRUD operations: create and update.
    """
    try:
        user = get_system_user()
        
        if created:
            # Contact created
            activity_type = 'client_added' if instance.type and instance.type.lower() == 'client' else 'prospect_added'
            title = 'Client ajouté' if activity_type == 'client_added' else 'Prospect ajouté'
            description = f"New {instance.type} contact created: {instance.name}"
            
            Activity.objects.create(
                title=title,
                description=description,
                type=activity_type,
                user=user,
                contact=instance,
            )
        else:
            # Contact updated
            Activity.objects.create(
                title='Contact mis à jour',
                description=f"Contact updated: {instance.name}",
                type='status_updated',
                user=user,
                contact=instance,
            )
    except Exception as e:
        print(f"Error tracking Contact activity: {str(e)}")


@receiver(post_delete, sender=Contact)
def track_contact_delete(sender, instance, **kwargs):
    """
    Track Contact deletion.
    """
    try:
        user = get_system_user()
        Activity.objects.create(
            title='Contact supprimé',
            description=f"Contact deleted: {instance.name}",
            type='other',
            user=user,
        )
    except Exception as e:
        print(f"Error tracking Contact deletion: {str(e)}")


@receiver(post_save, sender=Prospect)
def track_prospect_activity(sender, instance, created, **kwargs):
    """
    Track Prospect CRUD operations: create and update.
    """
    try:
        user = get_system_user()
        
        if created:
            # Prospect created
            Activity.objects.create(
                title='Prospect ajouté',
                description=f"New prospect created: {instance.entreprise}",
                type='prospect_added',
                user=user,
                prospect=instance,
            )
        else:
            # Prospect updated
            Activity.objects.create(
                title='Prospect mis à jour',
                description=f"Prospect updated: {instance.entreprise}",
                type='status_updated',
                user=user,
                prospect=instance,
            )
    except Exception as e:
        print(f"Error tracking Prospect activity: {str(e)}")


@receiver(post_delete, sender=Prospect)
def track_prospect_delete(sender, instance, **kwargs):
    """
    Track Prospect deletion.
    """
    try:
        user = get_system_user()
        Activity.objects.create(
            title='Prospect supprimé',
            description=f"Prospect deleted: {instance.entreprise}",
            type='other',
            user=user,
        )
    except Exception as e:
        print(f"Error tracking Prospect deletion: {str(e)}")
