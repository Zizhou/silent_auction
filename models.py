from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.utils import timezone
import datetime, uuid

# Create your models here.
# that I will

class Bid(models.Model):
    auction = models.ForeignKey("Auction")
    uuid = models.CharField(max_length = 200, unique = True, blank = True, null = True)
    amount = models.IntegerField(default = 0)
    email = models.EmailField()
    name = models.CharField(max_length = 200, unique = False, blank = True, null = True)
    bid_time = models.DateTimeField(default = timezone.now, editable = False) 
    troll = models.BooleanField(default = False, blank = True)
    

    def __unicode__(self):
        return unicode(self.bid_time) + unicode(self.auction.item_name) + ' ' + unicode(self.name) + ' ' + unicode(self.amount)

class Auction(models.Model):
    item_name = models.CharField(max_length = 200, unique = True)
    item_description = models.TextField(blank = True)
    top_bid = models.IntegerField(default = 0)
    uuid = models.CharField(max_length = 200, unique = True, blank = True, null = True)
    start_time = models.DateTimeField(default=timezone.now, editable=False)
    end_time = models.DateTimeField(default = timezone.now)
    active = models.BooleanField(default = True)
    #TODO image = models.ImageField(blah blah blah)
    
    def __unicode__(self):
        return unicode(self.item_name)

##Forms

#I totally forgot about modelforms. oops.
class BidForm(forms.Form):
    amount = forms.IntegerField(min_value = 0, label = 'Your Bid', widget = forms.NumberInput(attrs={'required': True}))
    email = forms.EmailField(label = 'Valid E-Mail Address', widget = forms.EmailInput(attrs={'required': True}))
    name = forms.CharField(max_length = 200, label = 'Your Name', widget = forms.TextInput(attrs={'required': True}))

    def save_bid(self, auction_id):
        bid = Bid(amount = self.cleaned_data['amount'], email = self.cleaned_data['email'], name = self.cleaned_data['name'], auction = Auction.objects.get(uuid = auction_id))
        bid.save()
        print bid.uuid
        uuid = bid.uuid
        return uuid
    #true if bid is above top and auction is active 
    #(also if it was prepared under supervision of a rabbi)
    def is_kosher(self, auction_id):
        this_auction = Auction.objects.get(uuid = auction_id)
        if this_auction.top_bid >= self.cleaned_data['amount']:
            return False
        if this_auction.active == False:
            return False
        return True
##magic signals
#magically delicious

class TrollForm(forms.Form):
    troll = forms.BooleanField(required = False, label = 'Troll Bid?')
    
    def toggle_troll(self, uuid):
        bid = Bid.objects.get(uuid = uuid)
        bid.troll = self.cleaned_data['troll']
        bid.save()
        print bid
        print bid.troll
        

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
    #update auction top bid every non-creation save
    else:
        top = instance.auction.bid_set.filter(troll = False).order_by('-amount')[0]
        instance.auction.top_bid = top.amount
        instance.auction.save()
post_save.connect(bid_create, sender = Bid)

#helper to create uuid if field empty
def create_uuid(item):
    if item.uuid == None or item.uuid == '':
        item.uuid = uuid.uuid4()
    item.save()
