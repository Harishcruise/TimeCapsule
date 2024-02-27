from django.utils import timezone
from TimeCapsuleManagement.models import Capsule
from django.core.exceptions import ObjectDoesNotExist


def create_capsule(owner_id, name, description, is_public, unsealing_date):
    """
    Create a new capsule.
    Args:
        owner_id: The ID of the UserProfile who owns the capsule.
        name: The name of the capsule.
        description: A description of the capsule.
        is_public: Boolean indicating if the capsule is public.
        unsealing_date: The date and time when the capsule will be unsealed.
    Returns:
        The newly created Capsule object or None in case of an error.
    """
    try:
        capsule = Capsule.objects.create(
            owner=owner_id,
            name=name,
            description=description,
            is_public=is_public,
            unsealing_date=unsealing_date
        )
        return capsule
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while creating the capsule: {e}")
        return None


def get_capsule_by_id(capsule_id):
    """
    Retrieve a specific capsule by its ID.
    Args:
        capsule_id: The ID of the capsule to retrieve.
    Returns:
        Capsule object if found, None otherwise.
    """
    try:
        return Capsule.objects.get(id=capsule_id)
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # Handle exceptions, such as database errors
        print(f"An error occurred while retrieving the capsule {capsule_id}: {e}")
        return None
