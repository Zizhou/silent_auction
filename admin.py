from django.contrib import admin

from silent_auction.models import Bid, Auction
# Register your models here.

class BidAdmin(admin.ModelAdmin):
    fields = ['auction', 'uuid', 'amount', 'email', 'name']

class AuctionAdmin(admin.ModelAdmin):
    fields = ['item_name', 'item_description', 'top_bid', 'uuid','active', 'end_time']

admin.site.register(Bid, BidAdmin)
admin.site.register(Auction, AuctionAdmin)
