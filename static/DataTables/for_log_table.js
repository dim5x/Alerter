$(document).ready(function () {
    $("#log").DataTable({
        // ajax: '/test',
        // columns:[
        //     {data: 'receivedat'},
        //     {data: 'priority'},
        //     {data: 'from_host'},
        //     {data: 'process'},
        //     {data: 'syslog_tag'},
        //     {data: 'mac_type'},
        //     {data: 'message'},
        //     {data: 'mac'},
        // ],
        "lengthMenu": [[50, 75, 100, -1], [50, 75, 100, "All"]],
        "order": [[ 0, "desc" ]]
    });
});
