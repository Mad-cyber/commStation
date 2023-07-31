// worked from google docs https://www.youtube.com/watch?v=c3MjU9E9buQ
let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: { 'country': ['irl'] },
        })
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


});
