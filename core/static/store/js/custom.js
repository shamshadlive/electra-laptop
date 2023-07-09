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


//password match check

function matchPassword(field1,field2) {  
    var pw1 = document.getElementById(field1);  
    var pw2 = document.getElementById(field2); 
    if(pw1.value != pw2.value)  
    {   
      return false
    } else {  
      return true
    }  
  }  




//UPDATE USER BASIC FIELDS 

function editFieldUserProfile(number) {
    element = document.getElementById('userProfileField' + number)
    element.readOnly=false;
    element.focus()
    element.setSelectionRange(element.value.length, element.value.length);
};

//first name and last name
function UpdateFieldUserProfile(field) {

        url = '/users/basic/update'
        var data = {
            field: field.name,
            value: field.value,

        };
        
        $.ajax({
            type: "POST",
            url: url,  // Replace with the actual URL for your view
            dataType: "json",
            data: JSON.stringify(data),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"), 
              },
            success: (data) => {
                console.log(data.status);
              },
            error: (error) => {
                alert(error)
              }
        });

};

//password change user
function UpdateFieldUserProfilePassword(get_old_password,get_password1,get_password2) {

        document.getElementById(get_old_password+'Error').innerText = ''
        document.getElementById(get_password1+'Error').innerText = ''
        document.getElementById(get_password2+'Error').innerText = ''

        var old_password = document.getElementById(get_old_password)
        var password1 = document.getElementById(get_password1)
        var password2 = document.getElementById(get_password2)

        if (!old_password.value){
          document.getElementById(get_old_password+'Error').innerText = 'Please Enter Password'
          return
        }

        if (!password1.value){
          document.getElementById(get_password1+'Error').innerText = 'Please Enter Password'
          return
        }

        if (!password2.value){
          document.getElementById(get_password2+'Error').innerText = 'Please Enter Password'
          return
        }

        if(matchPassword(get_password1,get_password2))
        {
          url = '/users/basic/changepassword'
          var data = {
            old_password: old_password.value,
            password2: password2.value,
          };
          
          $.ajax({
              type: "POST",
              url: url,  // Replace with the actual URL for your view
              dataType: "json",
              data: JSON.stringify(data),
              headers: {
                  "X-Requested-With": "XMLHttpRequest",
                  "X-CSRFToken": getCookie("csrftoken"), 
                },
                success: (data) => {
                  if (data.status === "success") {
                    // Password change success
                    console.log(data);
                    location.reload();
                } else {
                    // Password change error
                    console.log(data);
                    // Display the error message on the page
                    document.getElementById(get_old_password + 'Error').innerText =data.message;
                }
              },
              error: (xhr, status, error) => {
                  // Display the error message on the page
                  document.getElementById(get_old_password + 'Error').innerText = 'Error: ' + xhr.responseText;
                  console.log("error");
                  console.log(error);
              }
          });
          
        }
        else{
          document.getElementById(get_password2+'Error').innerText = 'Password Not Match'
        }

};


//password change user send mail 
function sendPasswordResetOtpMail() {
        document.getElementById('sendPasswordResetOtpMailSpinnner').classList.remove('d-none')
        document.getElementById('sendPasswordResetOtpMailBtn').classList.add('disabled')
        console.log("call");
        var url ='/users/resetpassword/verify/otp/'

        $.ajax({
            type: "POST",
            url: url,  // Replace with the actual URL for your view
            dataType: "json",
            // data: JSON.stringify(data),
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"), 
              },
              success: (data) => {
                if (data.status === "success") {
                  // Password change success
                  var inTwoMinutes = new Date(new Date().getTime() + 2 * 60 * 1000);
                  Cookies.set('can_otp_enter', 'True', { expires: inTwoMinutes, path: '/' });
                  window.location = data.redirect_url;
              } else {
                  // Password change error
                  console.log(data);
                  // Display the error message on the page
              }
                
            },
            error: (xhr, status, error) => {
                // Display the error message on the page
                console.log("error");
                console.log(error);
            }
        });
          

};


function sendEmailChangeOtpMail(){
  var new_email_id = document.getElementById('sendEmailChangeOtpMailNewMail')
  document.getElementById('sendEmailChangeOtpMailNewMailError').innerText = ''
  if (!new_email_id.value){
    document.getElementById('sendEmailChangeOtpMailNewMailError').innerText = 'Please enter a value'
    return
  }

  var url = '/users/update/email'

  var data = {
    new_email: new_email_id.value,
  };

  $.ajax({
    type: "POST",
    url: url,  // Replace with the actual URL for your view
    dataType: "json",
    data: JSON.stringify(data),
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"), 
      },
      success: (data) => {
        if (data.status === "success") {
          // email success
          console.log(data);
          document.getElementById('sendEmailChangeOtpMailNewMailOtpDiv').classList.remove('d-none')
          document.getElementById('sendEmailChangeOtpMailNewMailCnfBTn').classList.add('d-none')
          document.getElementById('sendEmailChangeOtpMailNewMail').setAttribute('readonly', true);

      } else {
          // Password change error
          console.log(data);
          document.getElementById('sendEmailChangeOtpMailNewMailError').innerText = data.message

          // Display the error message on the page
      }
        
    },
    error: (xhr, status, error) => {
        // Display the error message on the page
        console.log("error");
        console.log(error);
    }
});
  
}

function sendEmailChangeOtpMailVerify(){
  console.log("ok");
  var new_email_id = document.getElementById('sendEmailChangeOtpMailNewMail')
  var otp = document.getElementById('sendEmailChangeOtpMailNewMailOtp')

  document.getElementById('sendEmailChangeOtpMailNewMailOtpError').innerText = ''
  if (!otp.value){
    document.getElementById('sendEmailChangeOtpMailNewMailOtpError').innerText = 'Please enter a value'
    return
  }

  var url = '/users/update/email/verify'

  var data = {
    new_email: new_email_id.value,
    otp : otp.value
  };

  $.ajax({
    type: "POST",
    url: url,  // Replace with the actual URL for your view
    dataType: "json",
    data: JSON.stringify(data),
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"), 
      },
      success: (data) => {
        if (data.status === "success") {
          // email success
          console.log(data);
          location.reload();

      } else {
          // Password change error
          console.log(data);
          document.getElementById('sendEmailChangeOtpMailNewMailOtpError').innerText = data.message

          // Display the error message on the page
      }
        
    },
    error: (xhr, status, error) => {
        // Display the error message on the page
        console.log("error");
        console.log(error);
    }
});
  
}





function sendMobChangeOtp(){
  var new_mobile = document.getElementById('sendMobileChangeOtpMobNewMob')
  document.getElementById('sendMobileChangeOtpMobNewMobError').innerText = ''
  if (!new_mobile.value){
    document.getElementById('sendMobileChangeOtpMobNewMobError').innerText = 'Please enter a value'
    return
  }

  var url = '/users/update/mobile'

  var data = {
    new_mobile: new_mobile.value,
  };

  $.ajax({
    type: "POST",
    url: url,  // Replace with the actual URL for your view
    dataType: "json",
    data: JSON.stringify(data),
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"), 
      },
      success: (data) => {
        if (data.status === "success") {
          // email success
          console.log(data);
          document.getElementById('sendMobileChangeOtpMobNewMobOtpDiv').classList.remove('d-none')
          document.getElementById('sendMobileChangeOtpMobNewMobCnfBTn').classList.add('d-none')
          document.getElementById('sendMobileChangeOtpMobNewMob').setAttribute('readonly', true);
         

      } else {
          // Password change error
          console.log(data);
          document.getElementById('sendMobileChangeOtpMobNewMobOtpError').innerText = data.message

          // Display the error message on the page
      }
        
    },
    error: (xhr, status, error) => {
        // Display the error message on the page
        console.log("error");
        console.log(error);
    }
});
  
}



function sendMobChangeOtpVerify(){
  var new_mobile = document.getElementById('sendMobileChangeOtpMobNewMob')
  var otp = document.getElementById('sendMobileChangeOtpMobNewMobOtp')

  document.getElementById('sendMobileChangeOtpMobNewMobOtpError').innerText = ''
  if (!otp.value){
    document.getElementById('sendMobileChangeOtpMobNewMobOtpError').innerText = 'Please enter a value'
    return
  }

  var url = '/users/update/mobile/verify'

  var data = {
    new_mobile: new_mobile.value,
    otp : otp.value
  };

  $.ajax({
    type: "POST",
    url: url,  // Replace with the actual URL for your view
    dataType: "json",
    data: JSON.stringify(data),
    headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCookie("csrftoken"), 
      },
      success: (data) => {
        if (data.status === "success") {
          // email success
          console.log(data);
          location.reload();

      } else {
          // Password change error
          console.log(data);
          document.getElementById('sendEmailChangeOtpMailNewMailOtpError').innerText = data.message

          // Display the error message on the page
      }
        
    },
    error: (xhr, status, error) => {
        // Display the error message on the page
        console.log("error");
        console.log(error);
    }
});
  
}


