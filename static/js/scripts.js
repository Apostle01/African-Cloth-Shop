console.log("scripts.js loaded");

$(document).on('click', '#add-to-cart-btn', function(e) {
    e.preventDefault();
    
    let product_id = $(this).val();

    $.ajax({
        type: "POST",
        url: "/cart/add/",
        data: {
            product_id: product_id,
            csrfmiddlewaretoken: document.querySelector('[name=csrfmiddlewaretoken]').value,
            action: "post"
        },
        success: function (json) {
            console.log("Added to cart:", json);
        },
        error: function (xhr, errmsg, err) {
            console.log("AJAX Error:", errmsg);
        }
    });
});
