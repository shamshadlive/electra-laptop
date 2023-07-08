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




//UPDATE USER BASIC FIELDS 

function editFieldUserProfile(number) {
    element = document.getElementById('userProfileField' + number)
    element.readOnly=false;
    element.focus()
    element.setSelectionRange(element.value.length, element.value.length);
};

function UpdateFieldUserProfile(field) {
        alert(field.name)
        alert(field.value)
  //  element = document.getElementById('userProfileField' + number)
 //   element.readOnly=false;
    //element.focus()
 //   element.setSelectionRange(element.value.length, element.value.length);
};