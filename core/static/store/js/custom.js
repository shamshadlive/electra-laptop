// Function to retrieve the CSRF token from the cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}










// #Cancel User Order
function cancelUserOrder(order_number,user) {
    // var selectedOption = selectElement.options[selectElement.selectedIndex].text;
    // var data = {
    //     order_number: order_number,
    //     selected_option: selectedOption
    // };
    alert(order_number+user)
    // $.ajax({
    //     type: "POST",
    //     url: "change/status",  // Replace with the actual URL for your view
    //     dataType: "json",
    //     data: JSON.stringify(data),
    //     headers: {
    //         "X-Requested-With": "XMLHttpRequest",
    //         "X-CSRFToken": getCookie("csrftoken"), 
    //       },
    //     success: (data) => {
    //         console.log(data);
    //       },
    //     error: (error) => {
    //         console.log(error);
    //         alert(error)
    //       }
    // });
}