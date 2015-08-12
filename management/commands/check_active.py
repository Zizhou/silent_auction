##schedule this script with a cron or something for every minute?
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from silent_auction.models import Auction

class Command(BaseCommand):

    help = 'turns auctions off if they hit their expiry date'
    def handle(self, *args, **options):
        queryset = Auction.objects.filter(active = True)
        for x in queryset:
            if timezone.now() > x.end_time:
                x.active = False
                x.save()

