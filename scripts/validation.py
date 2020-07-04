import re

def has_all_keys(data):
    """
        Validation for all fields
        userId; salesForceId; consultant; consEmail; bizUnit; clientAcct
        capability; leadName; tmEmail; cmEmail; desc; stage; nextSteps
        dateSubmitted; clientContact; clientDept
    """
    expected_keys = ["userId", "salesForceId", "consultant", "consEmail",
                    "bizUnit", "clientAcct", "capability", "leadName",
                    "tmEmail", "cmEmail", "desc", "stage",
                    "dateSubmitted", "clientContact", "clientDept"]
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
    try:
        data["userId"] -6
        return True
    except:
        return False


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


def has_valid_date(data):
    """
        Current valid date format:
        2/25/2020  (M/D/YYYY)
    """
    regex = re.compile(r"((10)|(11)|(12)|\d)/\d\d{0,1}?/\d{4}")

    if re.fullmatch(regex, data["dateSubmitted"]) is None:
        return False
    else:
        return True