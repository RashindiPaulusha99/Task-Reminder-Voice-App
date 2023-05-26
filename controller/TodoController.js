loadAllTodos("all")

$("#btnPlus").click(function () {
    $("#addTaskPage").css('display','block');
    $("#addTaskBackground").css('display','block');
});

$("#btnCloseAddTask").click(function () {
    $("#addTaskPage").css('display','none');
    $("#addTaskBackground").css('display','none');
    $("#editTaskPage").css('display','none');
    $("#date").val('')
    $("#time").val('')
    $("#task").val('')
});

$("#btnCloseEditTask").click(function () {
    $("#addTaskPage").css('display','none');
    $("#editTaskPage").css('display','none');
    $("#addTaskBackground").css('display','none');
    $("#date").val('')
    $("#time").val('')
    $("#task").val('')
});

$("#btnAddTask").click(function (event) {

    if ($("#date").val() == "" || $("#time").val() == "" || $("#task").val() == ""){
        alert("All fields are required!")
    }else {

        var taskDetail = {
            date: $("#date").val(),
            time: $("#time").val(),
            task:$("#task").val(),
            status:"PENDING"
        }

        if (confirm("Do you want to add this task ?") == true) {

            $.ajax({
                url: "http://127.0.0.1:5000/task/save",
                method: "POST",
                crossDomain: true,
                contentType: "application/json",
                data: JSON.stringify(taskDetail),
                success: function (response) {
                    if (response.status == 200) {
                        alert("Successfully Added!");

                        $("#date").val('')
                        $("#time").val('')
                        $("#task").val('')

                        $("#addTaskPage").css('display', 'none');
                        $("#addTaskBackground").css('display', 'none');
                        loadAllTodos("all");
                    }
                },
                error: function (ob, statusText, error) {
                    alert(statusText);
                }
            });
        }else {
            $("#addTaskPage").css('display', 'none');
            $("#addTaskBackground").css('display', 'none');
        }

    }
});

$("#btnAll").click(function () {
    loadAllTodos("all");
});

$("#btnMonday").click(function () {
    loadAllTodos("Monday");
});

$("#btnTuesday").click(function () {
    loadAllTodos("Tuesday");
});

$("#btnWednesday").click(function () {
    loadAllTodos("Wednesday");
});

$("#btnThursday").click(function () {
    loadAllTodos("Thursday");
});

$("#btnFriday").click(function () {
    loadAllTodos("Friday");
});

$("#btnSaturday").click(function () {
    loadAllTodos("Saturday");
});

$("#btnSunday").click(function () {
    loadAllTodos("Sunday");
});

const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
];

function checkDate(date) {
    const test = Math.ceil((new Date(date).getTime() - new Date().getTime()) / (1000 * 3600 * 24));

    if ( test == 0){
        return "Today";
    }else if (test == 1){
        return "Tomorrow";
    }else if (test == -1){
        return "Yesterday";
    }else {
        return new Date(date).getDate();
    }
}

function checkStatus(date,status) {
    const test = Math.ceil((new Date(date).getTime() - new Date().getTime()) / (1000 * 3600 * 24));

    if(test == 0){
        return "DUE TODAY";
    }else if(test >= 1) {
        return "UPCOMING";
    }else if(test < 1 && status === "COMPLETED"){
        return "COMPLETED";
    }else {
        return "MISSING";
    }
}

function checkStatusColour(date,status) {
    const test = Math.ceil((new Date(date).getTime() - new Date().getTime()) / (1000 * 3600 * 24));

    if( test == 0){
        return "cornflowerblue";
    }else if (test >= 1) {
        return "#95a5a6";
    }else if (test < 1 && status == "COMPLETED"){
        return "lightseagreen";
    }else{
        return "#eb3b5a ";
    }
}

function getDayOfWeek(date) {
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const dayIndex = new Date(date).getDay();
    const dayOfWeek = daysOfWeek[dayIndex];
    return dayOfWeek;
}

function loadTodoList(data) {
    for (var responseKey of data) {
        tableRows(responseKey);
    }
}

function tableRows(responseKey) {
    let raw = `<tr><td>
                        <div class="member d-flex align-items-start">
                                <div class="w-25 h-100 row" style="border-right: 2px solid #37517e">
                                    <div class="row text-center pt-3"><h1 id="day" style="color: steelblue">${checkDate(responseKey.date)}</h1></div>
                                    <div class="row text-center"><h2 id="month" style="color: steelblue">${getDayOfWeek(responseKey.date)}</h2></div>
                                </div>
                                <br>
                                <div class="member-info ms-5">
                                    <h4>${new Date(responseKey.date).getDate() + " " + monthNames[new Date(responseKey.date).getMonth()] + " " + new Date(responseKey.date).getFullYear()}</h4>
                                    <span>${responseKey.time}</span>
                                    <p>${responseKey.task}</p>
                                    <div class="social">
                                        <a href="#"><i onclick="editTask('${responseKey.tId}', '${responseKey.date}', '${responseKey.time}', '${responseKey.task}', '${responseKey.status}')" class="fas fad fa-pen-square btnEdit"></i></a>
                                        <a href="#"><i onclick="deleteTask(${responseKey.tId})" class="fas fad fa-calendar-times"></i></a>
                                        <div class="badge rounded-pill shadow ms-3" id="badgeStatus" style="background-color: ${checkStatusColour(responseKey.date,responseKey.status)}">${checkStatus(responseKey.date,responseKey.status)}</div>
                                    </div>
                                </div>
                        </div>
                    </td></tr>`;
    $("#tblTasks tbody").append(raw);

}

function loadAllTodos(day) {

    $.ajax({
        url: "http://127.0.0.1:5000/get/todos",
        method: "GET",
        crossDomain: true,
        contentType: "application/json",
        success: function (response) {
            console.log(response.data)
            $("#tblTasks tbody").empty();

            if (day == "all"){
                loadTodoList(response.data);
            }else {
                for (var responseKey of response.data) {
                    if (getDayOfWeek(responseKey.date) == day){
                        tableRows(responseKey)
                    }
                }
            }

        },
        error: function (ob) {
        }
    });

}

var editId;

function editTask(id,date,time,task,status) {

    $("#editTaskPage").css('display', 'block');
    $("#addTaskPage").css('display', 'none');
    $("#addTaskBackground").css('display','block');

    $("#editDate").val(date);
    $("#editTime").val(time);
    $("#editTask").val(task);
    editId = id;
}

$("#btnEditTask").click(function (){

    if ($("#editDate").val() == "" || $("#editTime").val() == "" || $("#editTask").val() == ""){
        alert("All fields are required!")
    }else {
        var taskDetail = {
            id:editId,
            date: $("#editDate").val(),
            time: $("#editTime").val(),
            task: $("#editTask").val(),
            status: $("#status option:selected").text()
        }

        if (confirm("Are sure you want to edit this task ?") == true) {
            $.ajax({
                url: "http://127.0.0.1:5000/task/update",
                method: "PUT",
                crossDomain: true,
                contentType: "application/json",
                data: JSON.stringify(taskDetail),
                success: function (response) {
                    if (response.status == 200) {
                        alert("Successfully Updated!");

                        $("#editDate").val('')
                        $("#editTime").val('')
                        $("#editTask").val('')
                        $("#status").val('')

                        $("#editTaskPage").css('display', 'none');
                        $("#addTaskBackground").css('display','none');

                        loadAllTodos("all");
                    }
                },
                error: function (ob, statusText, error) {
                    alert(statusText);
                }
            });
        }else {
            $("#editTaskPage").css('display', 'none');
            $("#addTaskBackground").css('display','none');
        }
    }
});

function deleteTask(id) {

    if (confirm("Are sure you want to delete this task ?") == true) {
        $.ajax({
            url: "http://127.0.0.1:5000/task/delete",
            method: "DELETE",
            crossDomain: true,
            contentType: "application/json",
            data: JSON.stringify({id: id}),
            success: function (response) {
                if (response.status == 200) {
                    alert(response.message);

                    loadAllTodos("all");
                }
            },
            error: function (ob, statusText, error) {
                alert(statusText);
            }
        });
    }else {

    }
}