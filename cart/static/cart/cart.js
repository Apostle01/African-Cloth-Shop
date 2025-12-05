console.log("Cart JS loaded");

document.addEventListener("DOMContentLoaded", () => {
    const addBtn = document.getElementById("add-to-cart-btn");

    if (addBtn) {
        addBtn.addEventListener("click", function() {
            const productId = this.dataset.id;

            fetch("/cart/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
                },
                body: `product_id=${productId}`
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert(data.product + " added to cart!");
                }
            });
        });
    }
});
