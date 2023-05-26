$("#btnRegister").click(function () {

    if ($("#firstName").val() == "" || $("#lastName").val() == "" || $("#formEmail").val() == "" ||  $("#formPassword").val() == ""){
        alert("All fields are required!")
    }else {

        var regDetail = {
            firstName: $("#firstName").val(),
            lastName: $("#lastName").val(),
            email:$("#formEmail").val(),
            password: $("#formPassword").val()
        }

        $.ajax({
            url: "http://127.0.0.1:5000/register/save",
            method: "POST",
            crossDomain: true,
            contentType: "application/json",
            data: JSON.stringify(regDetail),
            success: function (response) {
                if (response.status == 200) {

                    $("#firstName").val('')
                    $("#lastName").val('')
                    $("#formEmail").val('')
                    $("#formPassword").val('')

                    $("#homePage").css('display','block');
                    $("#registerPage").css('display','none');
                    $("#loginPage").css('display','block');

                    alert("Successfully Registered!");
                }
            },
            error: function (ob, statusText, error) {
                alert(statusText);
            }
        });
    }
});

$("#btnLogin").click(function () {

    if ($("#email").val() == "" || $("#password").val() == ""){
        alert("All fields are required!")
    }else {
        var logDetail = {
            email:$("#email").val(),
            password: $("#password").val()
        }

        $.ajax({
            url: "http://127.0.0.1:5000/login",
            method: "POST",
            crossDomain: true,
            contentType: "application/json",
            data: JSON.stringify(logDetail),
            success: function (response) {
                if (response.status == 200) {

                    $("#email").val('')
                    $("#password").val('')

                    $("#loginPage").css('display','none');
                    $(".homeHeading").css('display','none');
                    $("#header").css('display','block');
                    $("#btnPlus").css('display','block');
                    $("#table").css('display','block');

                }else if (response.status == 401){
                    alert(response.message)
                }else if (response.status == 400){
                    alert(response.message)
                }
            },
            error: function (ob, statusText, error) {
                alert(statusText);
            }
        });
    }
});