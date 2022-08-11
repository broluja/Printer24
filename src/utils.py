""" Utility functions """
from config import MAIL_API_KEY, MAIL_SECRET_KEY, HOST_EMAIL


def generate_code(n):
    from random import randrange
    nums = [str(randrange(1, 10)) for _ in range(n)]
    return int(''.join(nums))


def send_email(receiver, subject=None, template=None, code=None, user=None):
    from mailjet_rest import Client
    mailjet = Client(auth=(MAIL_API_KEY, MAIL_SECRET_KEY), version='v3.1')
    code_part = f'<strong>{str(code)}</strong>' if code else ''
    data = {'Messages': [{'From': {'Email': HOST_EMAIL, 'Name': 'Printer24.Admins'},
                          'To': [{'Email': receiver, 'Name': user or 'User'}],
                          'Subject': subject, 'TextPart': 'Greetings from Printer24.net',
                          'HTMLPart': template + code_part}]}

    mailjet.send.create(data=data)
