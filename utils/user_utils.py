import uuid

def get_user_id(cookies):
    user_id = cookies.get("user_id")

    if not user_id:
        user_id = str(uuid.uuid4())
        cookies["user_id"] = user_id
        cookies.save()

    return user_id