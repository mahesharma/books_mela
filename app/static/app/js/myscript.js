$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

function result(res, id, Qid) {

    $.ajax({
        type: "GET",
        url: "/plusminuscart",
        data: {
            pk: res,
            prod_id: id
        },
        success: function(data) {
            Qid.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount
            document.getElementById("total").innerText = data.total
            if (res == 3) {
                Qid.parentNode.parentNode.parentNode.parentNode.remove()
            }

        }


    })
}

$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var Qid = this.parentNode.children[2];
    result(1, id, Qid);
})
$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var Qid = this.parentNode.children[2];
    result(2, id, Qid);
})
$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var Qid = this
    result(3, id, Qid);

})