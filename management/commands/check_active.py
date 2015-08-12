##schedule this script with a cron or something for every minute?
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from silent_auction.models import Auction
from silent_auction import mailbot

class Command(BaseCommand):

    help = 'turns auctions off if they hit their expiry date'
    def handle(self, *args, **options):
        queryset = Auction.objects.filter(active = True)
        for x in queryset:
            if timezone.now() > x.end_time:
                x.active = False
                x.save()
                bids = x.bid_set.order_by('-amount')
                if len(bids) > 0:
                    winner = bids[0]
                    message = "Congratulations! You won the auction for " + unicode(x.item_name) + " with a bid of " + unicode(winner.amount) + ". Make your donation at [website here] as soon as possible."
                    subject = "Auction for " + unicode(x.item_name) + ":A winner is you!"
                    mail = mailbot.pack_MIME(message, winner.email, subject)
                    mailbot.send_mail(mail, winner.email)
                    print mail
