$( document ).ready(function() {
    /******* Common Email Format Validation - Starts here *********/
    jQuery.validator.addMethod("email", function(value, element) {
      // allow any non-whitespace characters as the host part
      return this.optional( element ) || /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/.test( value );
    }, 'Please enter a valid email address.');
    
    /******* Common Email Format Validation - Ends here *********/
    
    /******* Common Password Validation - Starts here *********/
    $.validator.addMethod("new_password1", function(value, element) {
        return this.optional(element) || /^[A-Za-z0-9\d=!\-@._*]+$/.test(value);
    }, "Please enter only alphabets or  numbers.");
     /******* Common Password Validation - Ends here *********/

// validation for Login Page starts here
    validator = $("#logn_form").validate({
        rules: {
            username: {
                required: true,
            },
             password: {
                 required: true,
                 minlength: 8
             },
        },
        messages: {
            username: {
                required: "This field is required"
            },
            password: {
                 required: "This field is required",
                 minlength: "Password should be atleast 8 characters",
            },
        },
    });
// validation for Login Page ends here


// validation for change Password starts here
    validator = $("#chang_pswd").validate({
        rules: {
            old_password: {
                required: true,
            },
             new_password1: {
                 required: true,
                 minlength: 8
             },
            new_password2: {
                required: true,
                equalTo : '#newpassword1'
            },
        },
        messages: {
            old_password: {
                required: "This field is required"
            },
             new_password1: {
                 required: "This field is required",
                 minlength: "Password should be atleast 8 characters",
             },
            new_password2: {
                required: "This field is required",
                equalTo : "Confirm Password should be same as New Password."
            },
        },
    });
// validation for change Password ends here

// validation for Reset password starts here
//     validator = $("#reset_psw").validate({
//         rules: {
//              new_password1: {
//                  required: true,
//                  minlength: 8
//              },
//             new_password2: {
//                 required: true,
//                 equalTo : '#newpassword1'
//             },
//         },
//         messages: {
//              new_password1: {
//                  required: "This field is required",
//                  minlength: "Password should be atleast 8 characters",
//              },
//             new_password2: {
//                 required: "This field is required",
//                 equalTo : "Confirm Password should be same as New Password."
//             },
//         },
//     });
// validation for change  Reset password  ends here

// validation for forgot Password starts here
    validator = $("#frgt_pswd").validate({
        rules: {
            email: {
                required: true,
            },
        },
        messages: {
            email: {
                required: "This field is required",
            },
        },
    });
// validation for forgot Password ends here

// slide show

$(".quick_links_block").ready(function() {
    $("#quickLinks").owlCarousel({
        autoPlay: 1000,loop: true,
        items : 1, // THIS IS IMPORTANT
        nav : true,
        dots : false,
        responsive : {
              480 : { items : 1  }, // from zero to 480 screen width 4 items
              768 : { items : 3  }, // from 480 screen widthto 768 6 items
              1024 : { items : 5   // from 768 screen width to 1024 8 items
              }
          },
    });
});

$(".logo_section_block").ready(function() {
    $("#logoSection").owlCarousel({
        autoPlay: 1000,
        loop: false,
        items : 1, // THIS IS IMPORTANT
        nav : true,
        dots : false,
        responsive : {
              480 : { items : 1  }, // from zero to 480 screen width 4 items
              768 : { items : 3  }, // from 480 screen widthto 768 6 items
              1025 : { items : 4   // from 768 screen width to 1024 8 items
              }
          },
    });
});



});