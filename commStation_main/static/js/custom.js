// worked from google docs https://www.youtube.com/watch?v=c3MjU9E9buQ
let autocomplete;
let geocoder; // Define the geocoder variable

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: { 'country': ['irl'] },
        });
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else {
        console.log('place name=>', place.name)
    }
    //get address and assign them to fields

    // Check if the geocoder is defined
    if (!geocoder) {
        geocoder = new google.maps.Geocoder();
    }

    // Get the address from the place object
    var address = place.formatted_address;

    // Use the geocoder to get the latitude and longitude
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // console.log('lat=>', latitude);
            // console.log('lng=>', longitude);
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);
            $('#id_address').val(address);
        }
    });
    //add address fields to form for bus dashboard
    console.log(place.address_components);
    for (var i = 0; i < place.address_components.length; i++) {
        for (var j = 0; j < place.address_components[i].types.length; j++) {
            //get city
            if (place.address_components[i].types[j] == 'locality') {
                $('#id_city').val(place.address_components[i].long_name);
            }
            //get post code
            if (place.address_components[i].types[j] == 'postal_code') {
                $('#id_post_code').val(place.address_components[i].long_name);
            }

            //get country field
            if (place.address_components[i].types[j] == 'country') {
                $('#id_country').val(place.address_components[i].long_name);
            }

        }
    }


}


$(document).ready(function () {
    // add item to cart
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();

        var menu_id = $(this).attr('data-id');
        var url = '/marketplace/add_to_cart/' + menu_id + '/'; // Make sure the URL is set correctly

        var data = {
            menu_id: menu_id,
        }

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    Swal.fire({
                        title: response.message,
                        text: '',
                        icon: 'warning'
                    }).then(function () {
                        window.location = '/accounts/login/';

                    })
                } if (response.status == 'Failed') {
                    Swal.fire({
                        title: response.message,
                        text: '',
                        icon: 'error'
                    })

                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + menu_id).html(response.qty);

                    //handle cart calculation and totals
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        })
    })

    //place cart item quantity for the menu
    $('.item_qty').each(function () {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        //console.log(qty) for testing the cart value appearing
        $('#' + the_id).html(qty)
    })

    //remove item from cart
    $('.remove_cart_item').on('click', function (e) {
        e.preventDefault();

        var menu_id = $(this).attr('data-id');
        var url = $(this).attr('data-url');
        var cart_id = $(this).attr('id');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    Swal.fire({
                        title: response.message,
                        text: '',
                        icon: 'warning'
                    }).then(function () {
                        window.location = '/accounts/login/';

                    })
                } else if (response.status == 'Failed') {
                    Swal.fire({
                        title: response.message,
                        text: '',
                        icon: 'error'
                    })
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + menu_id).html(response.qty);

                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax_dict'],
                        response.cart_amount['grand_total']
                    )

                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();

                    }


                }

            }
        })
    })

    $(document).ready(function () {
        //delete cart item from cart.html view
        $('.delete_cart').on('click', function (e) {
            e.preventDefault();

            var cart_id = $(this).attr('data-id');
            var url = $(this).attr('data-url');

            $.ajax({
                type: 'GET',
                url: url,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function (response) {
                    console.log(response);
                    if (response.status == 'Failed') {
                        Swal.fire({
                            title: response.message,
                            text: '',
                            icon: 'error'
                        });
                    } else {
                        $('#cart_counter').html(response.cart_counter['cart_count']);
                        Swal.fire({
                            title: response.status,
                            text: response.message,
                            icon: 'success'
                        });
                        applyCartAmounts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax-dict'],
                            response.cart_amount['grand_total']
                        )


                        removeCartItem(0, cart_id);
                        checkEmptyCart();

                    }
                }
            });
        });
    });

    //show instant deletion
    function removeCartItem(cartItemQty, cart_id) {
        if (cartItemQty <= 0) {
            //remove the cart element
            document.getElementById("cart-item-" + cart_id).remove()
        }




    }

    //check if cart is empty
    function checkEmptyCart() {
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter == 0) {
            document.getElementById("empty-cart").style.display = "block";
        }
    }

    //apply cart amounts
    function applyCartAmounts(subtotal, tax_dict, grand_total) {
        if (window.location.pathname == '/cart/') {
            $('#subtotal').html(subtotal)
            $('#total').html(grand_total)

            for(key1 in tax_dict){
                for(key2 in tax_dict[key1]){
                    console.log(tax_dict[key1][key2])
                    $('#fee-' + key1).html(tax_dict[key1][key2])
                    console.log('Key1:', key1);
                    console.log('Selector:','#fee-' + key1);
                    console.log('Value:', tax_dict[key1][key2]);

                }

            }
        }


    }
    //add the opening hours to the business dashboard
    $('.add_hour').on('click', function (e) {
        e.preventDefault();
        //alert('test');
        var day = document.getElementById('id_day').value;
        var from_hour = document.getElementById('id_from_hour').value;
        var to_hour = document.getElementById('id_to_hour').value;
        var is_closed = document.getElementById('id_is_closed').checked;
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        var url = document.getElementById('add_hour_url').value;

        console.log(day, from_hour, to_hour, is_closed, csrf_token);

        var condition = false;

        if (is_closed) {
            is_closed = 'True';
            if (day !== '') {
                condition = true;
            }
        } else {
            is_closed = 'False';
            if (day !== '' && from_hour !== '' && to_hour !== '') {
                condition = true;
            }
        }

        if (eval(condition)) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token,
                },
                success: function (response) {
                    if (response.status == 'success') {
                        if (response.is_closed == 'Closed') {
                            html = html = '<tr id="hour-' + response.id + '"><td><b>' + response.day + '</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="accounts/business/openhours/' + response.id + '/">Remove</a></td></tr>';
                        } else {
                            html = '<tr><td><b>' + response.day + '</b></td><td>' + response.from_hour + '-' + response.to_hour + ' </td><td><a href="#" class="remove_hour" data-url="accounts/business/openhours/' + response.id + '/">Remove</a></td></tr>';
                        }

                        $(".table-openhours").append(html)
                        document.getElementById("open_hours").reset();
                    } else {
                        console.log(response.error)
                        Swal.fire({
                            title: response.message,
                            text: 'error',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });

                    }
                }
            })

        } else {
            Swal.fire({
                title: 'Please fill all fields',
                text: '',
                icon: 'info',
                confirmButtonText: 'OK'
            });
        }
    });

    //remove the opening hour
    $(document).on('click', '.remove_hour', function (e) {
        e.preventDefault();
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == 'success') {
                    document.getElementById('hour-' + response.id).remove()
                }
            }

        })

    })


    //end of document
});
