from django.core.management import call_command
from django.utils.six import StringIO
from django.core import mail

def test_with_client(client):
    response = client.get('/en/')
    assert response.status_code == 200

def test_email_command():
    assert len(mail.outbox) == 0

    out = StringIO()
    call_command("email", stdout=out)

    assert len(mail.outbox) == 1
