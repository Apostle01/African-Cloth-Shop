console.log("scripts.js loaded");

$(document).on("click", "#add-to-cart-btn", function (e) {
    e.preventDefault();

    const productId = $(this).data("product-id");
    const quantity = $("#quantity").val();
    const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
    ).value;

    $.ajax({
        type: "POST",
        url: "/cart/add/",
        data: {
            product_id: productId,
            quantity: quantity,
            csrfmiddlewaretoken: csrfToken,
            action: "post"
        },

        success: function (json) {
            console.log("Added to cart:", json);

            // Update cart count
            const cartQuantity = document.getElementById("cart_quantity");

            if (cartQuantity) {
                cartQuantity.textContent = json.cart_total;
            }
        },

        error: function (xhr, errmsg, err) {
            console.error("AJAX Error:", errmsg, err);
        }
    });
});
