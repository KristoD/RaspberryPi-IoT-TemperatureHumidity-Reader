$(document).ready(() => {
    $.get('https://vwyr13xwu5.execute-api.us-east-1.amazonaws.com/test/get-all-temp-readings', (data) => {
        for(let i = 0; i < data.body.Items.length; i++) {
            $('tbody').append("<tr><td>"+new Date(data.body.Items[i].time_stamp * 1000)+"</td><td>"+data.body.Items[i].temperature+
            "</td><td>"+data.body.Items[i].humidity+"%</td></tr>");
        }
    });
});