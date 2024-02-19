import pyotp
from django.conf import settings


def verify_totp(token):
    """
    Verifies the given TOTP (Time-Based One-Time Password) token.

    :param token: The TOTP token to be verified.
    :type token: str

    :return: True if the TOTP token is valid, False otherwise.
    :rtype: bool
    """
    return pyotp.TOTP(settings.OTP_SECRET_KEY).verify(token)


def get_otpauth_url():
    """
    This method returns the OTPAuth URL for the Telegram bot.

    :return: OTPAuth URL
    :rtype: str
    """
    return pyotp.TOTP(settings.OTP_SECRET_KEY).provisioning_uri(
        name='@avivi_internship_bot',
        issuer_name='Aviv internship'
    )
