$(document).ready(function () {
    $('#log').DataTable({
        "lengthMenu": [[50, 75, 100, -1], [50, 75, 100, "All"]],
        "order": [[ 0, "desc" ]]
    });
});
