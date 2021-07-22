import pytest

from users.tasks import send_email


def test_send_email(mailoutbox, settings, email_fix, short_text, long_text):
    send_email(email_fix, subject=short_text, message=long_text)
    assert len(mailoutbox) == 1
    message = mailoutbox[0]
    assert message.from_email == settings.DEFAULT_FROM_EMAIL
    assert message.subject == short_text
    assert message.body == long_text


def test_send_email_no_content(mailoutbox, email_fix):
    send_email(email_fix)
    assert len(mailoutbox) == 1
    message = mailoutbox[0]
    assert message.subject == ''
    assert message.body == ''
