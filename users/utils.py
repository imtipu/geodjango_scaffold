from django.core.mail import send_mail
from django.conf import settings
import hashlib


def generate_md5_hash(text):
    return hashlib.md5(str(text).encode('utf-8')).hexdigest()


def send_password_reset_email(email, otp):
    try:
        send_mail(
            'Password Reset OTP',
            'Use this code: %s to reset your password' % otp,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True

    except Exception as e:
        return False


def calculate_age(date_of_birth):
    from dateutil import relativedelta
    from datetime import datetime
    age = relativedelta.relativedelta(datetime.today(), date_of_birth)
    return age
