from django.contrib.auth import get_user_model


def create_user(username, email, password, bio=None):
    """
    Create a new user with the given username, email, password, and optional bio.

    Args:
        username (str): The username for the new user.
        email (str): The email address for the new user.
        password (str): The password for the new user.
        bio (str, optional): An optional bio for the new user.

    Returns:
        The newly created user object or None if the creation failed.
    """
    user = get_user_model()
    try:
        user = user.objects.create(
            username=username,
            email=email,
            bio=bio  # Assuming your user model has a `bio` field
        )
        user.set_password(password)  # This correctly hashes the password before saving
        user.save()
        return user
    except Exception as e:
        print(f"An error occurred while creating the user: {e}")
        return None
