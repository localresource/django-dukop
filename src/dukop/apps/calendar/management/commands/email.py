import sys
import logging
import uuid
import secrets
import json

from django.conf import settings
from django.core.mail import send_mail as django_core_send_mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.translation import activate
from django.utils.translation import deactivate
from django.utils.translation import gettext as _

class EmailDigest:
    """
    Turn events into email-friendly content
    """
    def __init__(self, receiving_address, events):
        """
        receiving_address: Digest will be sent to this address
        events: List of events that will be in the digest
        """
        self._receiving_address = receiving_address
        self._events = events

    def receiving_address(self):
        return self._receiving_address

    def email_body_text(self):
        return render_to_string(
            'emails/email_digest.txt', # TODO Add this template
            self.as_template_context(),
        )

    def email_body_html(self):
        return render_to_string(
            'emails/email_digest.html', # TODO Add this template
            self.as_template_context(),
        )

    def email_subject(self):
        return "" # TODO Implement this

    def as_template_context(self):
        # TODO Implement this
        return {
            "var": "value"
        }

class SendEmailDigest:
    def __init__(self, connection = None, logger = None):
        if connection == None:
            # TODO Create a connection
            # connection = ...
            pass
        self.connection = connection

        if logger == None:
            logger = logging.getLogger('send_email')
        self.logger = logger

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG) # TODO Set correct level

    def send(self, email_digest):
        """
        Send an email to the specified email address.
        """

        log_entry_uuid = uuid.UUID(bytes=secrets.token_bytes(16)).hex

        try:
            subject = email_digest.email_subject()
            body_text = email_digest.email_body_text()
            body_html = email_digest.email_body_html()
            #sender = settings.EMAIL_SENDER, # TODO Add this setting
            sender = "local@localhost.localdomain"
            receiving_address = email_digest.receiving_address()

            self.logger.debug(
                "Sending email: {json}".format(
                    json=json.dumps({
                        "log_entry_uuid": log_entry_uuid,
                        "sender": sender,
                        "receiving_address": receiving_address,
                        "email_subject": subject,
                        "email_body_text": body_text,
                        "email_body_html": body_html,
                    })))
        except Exception as e:
            try:
                self.logger.error((
                    "Bad data in email digest? Bad configuration? "
                    "(log_entry_uuid={log_entry_uuid},"
                    "receiving_address={receiving_address}): {exception}"
                    ).format(
                        exception=e,
                        log_entry_uuid=str(locals().get("log_entry_uuid")),
                        receiving_address=str(locals().get("receiving_address")),
                    ))
                raise
            except Exception as ee:
                # Failed to log error. Giving up!
                raise

        try:
            django_result = django_core_send_mail(
                subject,
                body_text,
                sender,
                [receiving_address],
                connection=self.connection,
                html_message=body_html,
            )

            self.logger.debug(
                "Django send email result: {json}".format(
                    json=json.dumps({
                        "log_entry_uuid": log_entry_uuid,
                        "django_result": django_result,
                    })))
        except Exception as e:
            self.logger.error(
                ("Error occured while sending email "
                 "(log_entry_uuid={log_entry_uuid}): {exception}").format(
                     exception=e,
                     log_entry_uuid=log_entry_uuid,
                 ))
            raise

class Command(BaseCommand):
    help = (
            'Send emails'
            )

    def handle(self, *args, **options):
        self._setup_logger()

        self.logger.info("handle called!")

        # TODO Put the actual logic here
        for digest_subscriber in [None]:
            email_digest = EmailDigest(receiving_address="a@b.c",events=[])
            self.send_mail(email_digest)

    def _setup_logger(self):
        self.logger = logging.getLogger('dukop_email')

        if not self.logger.handlers:
            handler = logging.StreamHandler(self.stdout)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.DEBUG) # TODO Set correct level

    def send_mail(self, email_digest):
        """Send an email"""
        SendEmailDigest(logger=self.logger).send(email_digest)
