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

// Call the announceTasks function every 1 minute (60000 milliseconds)
setInterval(announceTasks, 20000);

function announceTasks() {
    var currentDate = new Date();

    // Get the year, month, and day from the current date
    var year = currentDate.getFullYear();
    var month = currentDate.getMonth() + 1; // Note: Months are zero-based, so January is 0
    var day = currentDate.getDate();

    // Format the date as 'YYYY-MM-DD'
    var formattedDate = year + '-' + month.toString().padStart(2, '0') + '-' + day.toString().padStart(2, '0');

    // Get the hours, minutes, and seconds from the current time
    var hours = currentDate.getHours();
    var minutes = currentDate.getMinutes();
    var seconds = currentDate.getSeconds();

    // Format the time as 'HH:MM:SS'
    var formattedTime = hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0') + ':' + '00';

    $.ajax({
        url: "http://127.0.0.1:5000/get/todos",
        method: "GET",
        crossDomain: true,
        contentType: "application/json",
        success: function (response) {
            if (response.status == 200){
                for (var responseKey of response.data) {

                    if (responseKey.date == formattedDate && responseKey.time == formattedTime){
                        speakText(responseKey.task);
                    }
                }
            }
        },
        error: function (ob) {
        }
    });

}

// Function to speak the provided text using text-to-speech
function speakText(text) {
    if ('speechSynthesis' in window) {
        var msg = new SpeechSynthesisUtterance();
        msg.text = text.replace(/\bI\b/g, 'you').replace(/\bmy\b/g, 'your');
        msg.rate = 0.5;
        window.speechSynthesis.speak(msg);
    } else {
        // Speech synthesis not supported
        console.log('Speech synthesis is not supported in this browser.');
    }
}

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

                    announceTasks()

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