
function setPrice(auction_id){
    $.get('/silent_auction/api/auction/' + auction_id, function(data){
        $('#price').html(data);
    });
    console.log(parseInt($('#price').text()));

}

//timer thing?
var timer;
function repeatMe(auction_id){
    timer = setInterval(function(){setPrice(auction_id)},5000);
}

//instant pre-validation
function checkBid(auction_id){
    var valid = false;
    setPrice(auction_id);//this is jank
    
    if ($('#id_amount').val() > parseInt($('#price').text())){
        valid = true
    }
    else{
        alert('Bid too low! Current top bid at ' + parseInt($('#price').text()))
        valid = false
    }

    return valid
}

