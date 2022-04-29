import re

# 권은경
def validate_email(email):
    return re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

def validate_phone(phone):
    return re.match('\d{3}-\d{3,4}-\d{4}', phone)

def validate_id(advertiser_id):
    return re.match('^\d{8}$', advertiser_id)

    