from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import datetime, uuid

# Create your models here.
# that I will

class Bid(models.Model):
    auction = models.ForeignKey("Auction")
    uuid = models.CharField(max_length = 200, unique = True, blank = True, null = True)
    amount = models.IntegerField(default = 0)
    email = models.EmailField()
    name = models.CharField(max_length = 200, unique = False, blank = True, null = True)
    bid_time = models.DateTimeField(default = datetime.datetime.now, editable = False) 
    
    def __unicode__(self):
        return unicode(self.bid_time) + unicode(self.auction.item_name) + ' ' + unicode(self.name) + ' ' + unicode(self.amount)

class Auction(models.Model):
    item_name = models.CharField(max_length = 200, unique = True)
    item_description = models.TextField(blank = True)
    top_bid = models.IntegerField(default = 0)
    uuid = models.CharField(max_length = 200, unique = True, blank = True, null = True)
    start_time = models.DateTimeField(default=datetime.datetime.now, editable=False)
    end_time = models.DateTimeField(default = datetime.datetime(2015,12,12,0,0,0,0,None))
    active = models.BooleanField(default = True)
    #TODO image = models.ImageField(blah blah blah)
    
    def __unicode__(self):
        return unicode(self.item_name)

##Forms

class BidForm(forms.Form):
    amount = forms.IntegerField(min_value = 0, label = 'Your Bid:')
    email = forms.EmailField(label = 'Valid E-Mail Address')
    name = forms.CharField(max_length = 200, label = 'Your Name')
    
    def save_bid(self, auction_id):
        bid = Bid(amount = self.cleaned_data['amount'], email = self.cleaned_data['email'], name = self.cleaned_data['name'], auction = Auction.objects.get(uuid = auction_id))
        bid.save()
        print bid.uuid
        uuid = bid.uuid
        return uuid
##magic signals
#magically delicious

#creates uuid for auctions upon successful creation
def auction_create(sender, instance, created, **kwargs):
    if created == True:
        create_uuid(instance)
post_save.connect(auction_create, sender = Auction)

#creates uuid for bids upon sucessful creation and emails bidder(todo)
def bid_create(sender, instance, created, **kwargs):
    if created == True:
        create_uuid(instance)
        #update top bid, should always run
        if instance.amount > instance.auction.top_bid:
            instance.auction.top_bid = instance.amount
            instance.auction.save()
        #TODO: email bidder

post_save.connect(bid_create, sender = Bid)

#helper to create uuid if field empty
def create_uuid(item):
    if item.uuid == None or item.uuid == '':
        item.uuid = uuid.uuid4()
    item.save()
