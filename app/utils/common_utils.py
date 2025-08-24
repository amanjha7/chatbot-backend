def clean_and_alternate_messages(messages):
    """
    Clean messages and ensure they alternate by role.

    Args:
        messages (list[dict]): Example:
            [
                {"role": "user", "content": "Hello   "},
                {"role": "user", "content": "  How are you?"},
                {"role": "assistant", "content": "I'm fine."},
                {"role": "assistant", "content": "   And you?   "}
            ]

    Returns:
        list[dict]: Cleaned, alternating-role messages.
    """
    cleaned = []
    last_role = None

    for msg in messages:
        role = msg.get("role", "").strip()
        content = " ".join(msg.get("content", "").split())  # remove extra spaces

        if not content:
            continue  # skip empty messages

        if cleaned and cleaned[-1]["role"] == role:
            # Merge into the last message if same role
            cleaned[-1]["content"] += " " + content
        else:
            cleaned.append({"role": role, "content": content})

        last_role = role

    return cleaned


def generate_uuid():
    import uuid
    return str(uuid.uuid4())

def hash_string(input_string):
    import hashlib
    return hashlib.sha256(input_string.encode()).hexdigest()
