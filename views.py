from django.shortcuts import render, HttpResponse, get_object_or_404, redirect

from silent_auction.models import Bid, Auction, BidForm

import datetime
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
    context = {
        'auction' : auction,
    }
    return render(request, 'silent_auction/auction.html', context)
##bid placement form
# bid on x auction, requires bid, valid email
# displays current top bid(auto update?)
def bid_form(request):
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            bid_id = bid_form.save_bid(request.GET.get('auction_id'))
            

            return redirect('/silent_auction/bid/' + unicode(bid_id))
        else:
            return HttpResponse('nope') 
    else:        
        auction_id = request.GET.get('auction_id')
        if auction_id == None:
            return redirect('/silent_auction/')
        auction = get_object_or_404(Auction.objects.filter(uuid = auction_id))
        context = {
            'form' : BidForm,
            'auction' : auction,
            'auction_id' : auction_id,
        }
        return render(request, 'silent_auction/bid_form.html', context)
##static bid page
# shows any given bid
# link sent to bidder in email, otherwise unlisted for public
def bid_page(request, bid_id):
    context = {
        'bid' : Bid.objects.get(uuid = bid_id),
        'bid_id' : bid_id,
    }
    return render(request, 'silent_auction/bid_page.html', context)

def api_price_check(request, auction_id):
    auction = Auction.objects.get(uuid = auction_id)
    #if datetime.datetime.now(tz = auction.end_time.tzinfo) > auction.end_time or datetime.datetime.now(tz = auction.start_time.tzinfo) < auction.start_time:
     #   return False
    return HttpResponse(auction.top_bid)
