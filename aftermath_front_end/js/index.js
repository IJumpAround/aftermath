$(document).ready(function () {
    console.log('done')
    $('#table_id').DataTable({
        select: true,
        dom: 'frtip',
        serverSide: true,
        columns:
            [
                {"data": "id", "visible": false},
                {"data": "model_type"},
                {"data": "name"},
                {"data": "text_description", "className": "truncate"},
                {"data": "rarity"},
                {"data": "wondrous"},
                {"data": "requires_attunement"},
                {"data": "player"},
                {"data": "quantity"},
                {"data": "model_name", "visible": false},
            ],

        ajax: {
            url: 'http://localhost:8000/items/',
            "contentType": 'application/json',
            "type": "POST",
            "data": function (d) {
                return JSON.stringify(d);
            },
            dataFilter: function(data){
                let json = jQuery.parseJSON( data );
                json.recordsTotal = json.resources.total_items;
                json.recordsFiltered = json.resources.total_items
                json.data = json.resources.data;

                return JSON.stringify( json ); // return JSON string
            },
        },



        createdRow: function (row) {
            var td = $(row).find(".truncate");
            td.attr("title", td.html());
        }
    });
    // call_backend()
});


function call_backend() {
    fetch('http://localhost:8000/items')
        .then(response => response.json())
        .then(data => console.log(data));
}