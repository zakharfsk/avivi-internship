from io import BytesIO

import qrcode

from apps.telegram_bot.bot.two_auth import get_otpauth_url


def get_qr_image():
    """

    This method generates a QR code image.

    Returns:
        bytes: The image data in bytes format.

    """
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    buffered = BytesIO()

    qr.add_data(get_otpauth_url())
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    img.save(buffered)

    return buffered.getvalue()
