import re

def has_all_keys(data):
    """
        Validation for all fields
        userID; recordID; consultant; consEmail; bizUnit; clientAcct
        capability; leadName; tmEmail; cmEmail; desc; status; nextSteps
        dateSubmitted
    """
    expected_keys = ["userID", "recordID", "consultant", "consEmail",
                    "bizUnit", "clientAcct", "capability", "leadName",
                    "tmEmail", "cmEmail", "desc", "status", "nextSteps",
                    "dateSubmitted"]
    actual_keys = data.keys()
    missing_keys = []
    for key in expected_keys:
        if key not in actual_keys:
            missing_keys.append(key)
    if len(missing_keys) == 0:
        return {"Valid": True, "Data": actual_keys} 
    else:
        return {"Valid": False, "Data": missing_keys}


def has_valid_ids(data):
    """
        userID should be int
        recordID should be int
        dateSubmitted should be in valid datetime format
        everything else should be strings
    """
    try:
        data["userID"] - 6
    except:
        return False

    try:
        data["recordID"] - 6
    except:
        return False
    return True


def has_valid_emails(data):
    """
        Validates all three e-mails.
        consEmail, tmEmail, and cmEmail.
    """

    emails = [data["consEmail"], data["tmEmail"], data["cmEmail"]]
    invalid_emails = []
    
    
    # ? Matches a string with one '@' before a '.' and has no spaces throughout.
    regex = re.compile(r"^[^@\s]+?@[^@\s]+?\.[^@\s]+$")
    
    # ? Returns None if string doesn't meet regex requirements.
    if re.fullmatch(regex, emails[0]) is None:
        invalid_emails.append(emails[0])

    if re.fullmatch(regex, emails[1]) is None:
        invalid_emails.append(emails[1])

    if re.fullmatch(regex, emails[2]) is None:
        invalid_emails.append(emails[2])
    
    if len(invalid_emails) == 0:
        return True
    else:
        return False