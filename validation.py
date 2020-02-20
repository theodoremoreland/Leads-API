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
        return {"Valid": "True", "Data": missing_keys} 
    else:
        return {"Valid": "False", "Data": missing_keys}


def has_correct_datatypes(data):
    """
        userID should be int
        recordID should be int
        dateSubmitted should be in valid datetime format
        everything else should be strings
    """
    try:
        int(data["userID"])
    except:
        return "userID not a valid number"

    try:
        int(data["recordID"])
    except:
        return "recordID not a valid number"

    return {"Valid": "True", "Data": [data["userID"], data["recordID"]]}


def has_valid_emails(data):

    invalid_emails = []

    # ! Matches a string with one '@' before a '.' and has no spaces throughout.
    regex = re.compile(r"^[^@\s]+?@[^@\s]+?\.[^@\s]+$")
    
    # ! Returns None is string doesn't meet regex requirements.
    if re.fullmatch(regex, data["consEmail"]) is None:
        invalid_emails.append(data["consEmail"])

    if re.fullmatch(regex, data["tmEmail"]) is None:
        invalid_emails.append(data["tmEmail"])

    if re.fullmatch(regex, data["cmEmail"]) is None:
        invalid_emails.append(data["cmEmail"])
    
    if len(invalid_emails) == 0:
        return {"Valid": "True", "Data": invalid_emails}
    else:
        return {"Valid": "False", "Data": invalid_emails}