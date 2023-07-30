// worked from google docs https://www.youtube.com/watch?v=c3MjU9E9buQ
let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        componentRestrictions: {'country': ['irl']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }






    // console.log(place.address_components)
    // for (var i=0; i<place.address_components.length; i++){
    //     for(var j=0; j<place.address_components[i].types.length; j++){
    //         //get the country
    //         if (place.address_components[i].types[j] =='country'){
    //             $('#id_country').val(place.address_components[i].long_name);
    //         }
    //     }

    // }
}
// console.log(address)
    // geocoder.geocode({'address':address}, function(results,status){
    //     // console.log('results=>', results)
    //     // console.log('status=>', status)
    //     if (status == google.maps.GeocoderStatus.OK){
            
    //     }

    // })

    $(document).ready(function () {
        //add item to cart
        $('.add_to_cart').on('click', function (e) {
            e.preventDefault();

            var menu_id = $(this).attr('data-id');
            var url = $(this).attr('data-url');

            var data = {
                menu_id: menu_id,
            }

            $.ajax({
                type: 'GET',
                url: url,
                data: data,
                success: function (response) {
                    console.log(response)
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+menu_id).html(response.qty);
                }
            })
        })

        //place cart item quantity for the menu
        $('.item_qty').each(function(){
            var the_id = $(this).attr('id')
            var qty = $(this).attr('data-qty')
            //console.log(qty) for testing the cart value appearing
            $('#'+the_id).html(qty)
        })

        //remove item from cart
        $('.remove_cart_item').on('click', function (e) {
            e.preventDefault();

            var menu_id = $(this).attr('data-id');
            var url = $(this).attr('data-url');

            $.ajax({
                type: 'GET',
                url: url,
                success: function (response) {
                    console.log(response)
                    // $('#cart_counter').html(response.cart_counter['cart_count']);
                    // $('#qty-'+menu_id).html(response.qty);
                }
            })
        })


    });
