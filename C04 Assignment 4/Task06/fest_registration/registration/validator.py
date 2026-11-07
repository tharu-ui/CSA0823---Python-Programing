def valid_email(email):
    if not email or email != email.strip():
        return False
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    if " " in email:
        return False
    return True

def validate_record(record):
    required = ("register_number", "name", "department")
    if any(not record[key] for key in required):
        return False, "register number, name and department are required"
    if not valid_email(record["email"]):
        return False, f"invalid e-mail '{record['email']}'"
    if not record["events"]:
        return False, "at least one event is required"
    return True, ""
