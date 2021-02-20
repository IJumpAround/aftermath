function format ( d ) {
    // `d` is the original data object for the row
    console.log('formatting')
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">'+
        '<tr>'+
        '<td>Full Description:</td>'+
        '<td>'+ d.text_description.replace(/(?:\r\n|\r|\n)/g, '<br>') + '</td>'+
        '</tr>'+
        '<tr>'+
        '<td>Type: </td>'+
        '<td class="model-type">'+d.model_type+'</td>'+
        '</tr>'+
        '<tr>'+
        '<td>Extra info:</td>'+
        '<td>And any further details here (images etc)...</td>'+
        '</tr>'+
        '</table>';
}


$(document).ready(function () {
    let table = $('#table_id').DataTable({
        // select: true,
        dom: 'frtip',
        serverSide: true,
        columns:
            [
            {   "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": '<i class="fas fa-chevron-right"></i>'
            },
            {"data": "model_type", visible: false},
            {"data": "name"},
            {"data": "text_description", "className": "truncate"},
            {"data": "rarity"},
            {"data": "wondrous", visible: false},
            {"data": "requires_attunement", "className": "attunement"},
            {"data": "player"},
            {"data": "quantity"},
            ],

        ajax: {
            url: 'http://localhost:8000/items/',
            "contentType": 'application/json',
            "type": "POST",
            "data": function (d) {
                let js_data = JSON.stringify(d)
                // console.log(d)
                return js_data
            },
            dataFilter: function(data){
                let json = jQuery.parseJSON( data );
                json.recordsTotal = json.resources.total_items;
                json.recordsFiltered = json.resources.total_items
                json.data = json.resources.data;
                let js_data = JSON.stringify(json)

                // console.log(js_data)
                return js_data; // return JSON string
            },
        },
        createdRow: function (row) {
            let td = $(row).find(".truncate");
            td.attr("title", td.html());
        }
    });

    // let tr = $(this).children('tr');
    let test = table.rows()
    // console.log(tr)
    console.log(test)
    $('#table_id tbody').on('click', 'td.details-control', function () {
        let tr = $(this).closest('tr');
        let row = table.row( tr );
        let cell = $(tr).children("td").first()

        let i = cell.children()
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
            i.removeClass('fas fa-chevron-down')
            i.addClass('fas fa-chevron-right')

        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown')
            i.removeClass('fas fa-chevron-right')
            i.addClass('fas fa-chevron-down')
            // cell.removeClass("fas fa-chevron-right")
            // cell.addClass("fas fa-chevron-down")
            // console.log(tr)
            // tr.addClass('fas fa-chevron-right')
        }
    } );
});



function call_backend() {
    fetch('http://localhost:8000/items')
        .then(response => response.json())
        .then(data => console.log(data));
}