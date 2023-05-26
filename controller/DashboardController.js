$("#registerPage").css('display','none');
$("#header").css('display','none');
$("#addTaskPage").css('display','none');
$("#addTaskBackground").css('display','none');
$("#editTaskPage").css('display','none');
$("#btnPlus").css('display','none');
$("#loginPage").css('display','block');
$("#table").css('display','none');
$(".homeHeading").css('display','block');

$("#email").focus();

$("#btnRegisterPage").click(function () {
    $("#registerPage").css('display','block');
    $("#loginPage").css('display','none');

    $("#firstName").focus();
});

$("#btnLoginPage").click(function () {
    $("#registerPage").css('display','none');
    $("#loginPage").css('display','block');

    $("#email").focus();
});