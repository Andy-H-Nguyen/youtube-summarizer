import uuid

def get_user_id(cookies):
    # Safely retrieve the 'user_id' cookie
    user_id = cookies.get("user_id")

    if not user_id:
        # If no user_id exists, generate a new one and set it in the cookies
        user_id = str(uuid.uuid4())
        cookies["user_id"] = user_id
        cookies.save()  # Ensure the cookie is saved

    return user_id