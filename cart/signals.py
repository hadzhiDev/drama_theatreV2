from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import TicketForSale


@receiver(post_save, sender=TicketForSale)
def order_item_post_save(sender, instance: TicketForSale, created, *args, **kwargs):
    if created:
        ticket = instance.ticket
        instance.price = ticket.type.price
        instance.save()