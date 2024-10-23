$(document).ready(function () {
    // var url  = window.location.href;
   
    });
    
    
    
    function validateLogin() {
        if ($("#txtusername").val() == '' || $("#txtpassword").val() == ''){
    
            if ( $("#txtusername").val() == ''){
                $('#txtusername').addClass('form-error')
                $("#spanusername").text("This field should not be empty") 
            }
    
            if ( $("#txtpassword").val() == ''){
                $('#txtpassword').addClass('form-error')
                $("#spanpassword").text("This field should not be empty")    
            }
            
            return false;
        }
    
    
    
        else {
    
            $('#loginform').submit()
        };
    
    };

    $('#txtusername').bind('click', function() {
        $('#txtusername').removeClass('form-error');
        $('#spanusername').text('');
    });
    
    
    $('#txtpassword').bind('click', () => {
        $('#txtpassword').removeClass('form-error')
        $('#spanpassword').text('')
        })
    
    $("#txtpassword").on("keypress", function (e) {
        var key = e.which || e.keyCode;
        if (key === 13) {
            postMessage();
            e.preventDefault();
        }
        });