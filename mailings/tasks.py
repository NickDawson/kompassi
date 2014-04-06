from __future__ import absolute_import

from celery import shared_task


@shared_task
def message_send(message_id, recipient_ids=None, resend=False):
    from .models import Message

    message = message.objects.get(pk=message_id)
    if recipient_ids is None:
        recipients = None
    else:
        recipients = Person.objects.filter(pk__in=recipient_ids)

    message.send(recipients, resend)