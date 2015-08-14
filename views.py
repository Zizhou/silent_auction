from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils import timezone
from silent_auction.models import Bid, Auction, BidForm, TrollForm

import datetime, mailbot

#very hardcoded
#much terrible
LAZY_TLD = 'devletter.net'

# Create your views here.

##main landing page
# lists all ongoing auctions, maybe completed ones?
def main_page(request):
    context = {
        'auctions' : Auction.objects.filter(active = True),
        'complete_auctions' : Auction.objects.filter(active = False),
    }
    return render(request, 'silent_auction/main_page.html', context)

##individual auction page
# item name, description, current price(auto update?),link to bid
def auction(request, auction_id):
    auction = get_object_or_404(Auction.objects.filter(uuid = auction_id))
    all_bids = auction.bid_set.all().filter(troll = False).order_by('-amount')
    troll_bids = auction.bid_set.all().filter(troll = True).order_by('-amount')
    if len(all_bids) > 0:
        winner = all_bids[0].name
    else:
        winner = 'NONE'
    context = {
        'auction' : auction,
        'bids' : all_bids,
        'trolls': troll_bids,
        'winner': winner,
    }
    return render(request, 'silent_auction/auction.html', context)
##bid placement form
# bid on x auction, requires bid, valid email
# displays current top bid(auto updates)
def bid_form(request):
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        auction = Auction.objects.get(uuid = request.GET.get('auction_id'))
        #structural validation
        if bid_form.is_valid():
            #logical validation
            if not bid_form.is_kosher(request.GET.get('auction_id')):
                return HttpResponse('your bid is no longer valid, try again')

            bid_id = bid_form.save_bid(request.GET.get('auction_id'))
            
            
            #mail time! I should stop using this
            #one of these days, google is going to completely deprecate this

            #laaaaazy
            message = "Hey " + unicode(bid_form.cleaned_data['name']) + ",<p>You've submitted a bid for " + unicode(auction.item_name) + " for the amount of " + unicode(bid_form.cleaned_data['amount']) + ".<p>Your bid page can be found <a href='" + unicode(LAZY_TLD) +"/silent_auction/bid/"  + unicode(bid_id) + "'>here</a>.<p>Thanks for bidding and good luck!"
            mail = mailbot.pack_MIME(message, bid_form.cleaned_data['email'], 'Your bid for ' + unicode(auction.item_name))
            print mail 
            mailbot.send_mail(mail, bid_form.cleaned_data['email']) 
            
            
            return redirect('/silent_auction/bid/' + unicode(bid_id))
        else:
            return HttpResponse('your bid is structurally <i>wrong</i>, somehow') 
    else: 
        auction_id = request.GET.get('auction_id')
        if auction_id == None:
            return redirect('/silent_auction/')
        auction = get_object_or_404(Auction.objects.filter(uuid = auction_id))
        #auto fill if logged in, saving precious seconds!
        if request.user.is_authenticated():
            form = BidForm(initial = {
                'amount': auction.top_bid + 1,
                'name' : request.user.username,
                'email' : request.user.email,
            })

        else:
            form = BidForm(initial = {
                'amount': auction.top_bid + 1,
            })
        context = {
            'form' : form,
            'auction' : auction,
            'auction_id' : auction_id,
        }
        return render(request, 'silent_auction/bid_form.html', context)
##static bid page
# shows any given bid
# link sent to bidder in email, otherwise unlisted for public
def bid_page(request, bid_id):
    if request.method == 'POST':
        form = TrollForm(request.POST)
        if form.is_valid():
            form.toggle_troll(bid_id)

    form = TrollForm
    this_bid = get_object_or_404(Bid.objects.filter(uuid = bid_id))
    context = {
        'form' : TrollForm(initial = {'troll':this_bid.troll}),
        'bid' : this_bid,
        'bid_id' : bid_id,
    }
    return render(request, 'silent_auction/bid_page.html', context)

# endpoint for janky ajax requests for live price updates
def api_price_check(request, auction_id):
    auction = Auction.objects.get(uuid = auction_id)
    #THIS IS LARGELY DEPENDENT ON PROPER TIME ZONES
    if timezone.now() > auction.end_time or timezone.now() < auction.start_time:
        return HttpResponse(False)
    return HttpResponse(auction.top_bid)
