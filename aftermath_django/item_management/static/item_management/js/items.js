function format(d) {
    // `d` is the original data object for the row
    console.log('formatting')
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Full Description:</td>' +
        '<td>' + d.text_description.replace(/(?:\r\n|\r|\n)/g, '<br>') + '</td>' +
        '</tr>' +
        '</table>';
}


$(document).ready(function () {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    const csrftoken = getCookie('csrftoken');


    let table = $('#table_id').DataTable({
        // select: true,
        dom: 'frtip',
        serverSide: true,
        order: [[1, 'desc']],
        columns:
            [
                {
                    "data": null,
                    "className": 'details-control',
                    "orderable": false,
                    "ordering": false,
                    "defaultContent": '<i class="fas fa-chevron-right"></i>'
                },
                {"data": "model_type", visible: false},
                {
                    "data": "name", "className": "name_column",
                    "render": function (data, type, row, meta) {
                        let id = row.id
                        let model_name = row.model_name
                        let loc = `/items/${model_name}/${id}`
                        return `<a href=${loc}>${data}</a>`
                    }
                },
                {"data": "text_description", visible: false},
                {"data": "rarity", visible: false},
                {"data": "wondrous", visible: false},
                {
                    "data": "requires_attunement", "className": "attunement_col icon",
                    "render": function (data, type, row, meta) {
                        let requires = data
                        let attuned = row.is_attuned

                        let placeholder = ""

                        if (requires && attuned) {
                            placeholder = "<i class='fas fa-lock attuned'/>"
                        } else if (requires) {
                            placeholder = '<i class="fas fa-lock-open"/>'
                        } else {
                            placeholder = '<i class="fas fa-times not-attunable"/>'
                        }
                        return placeholder
                    }
                },
                {"data": "player", "order": "asc"},
                {"data": "quantity"},
                {"data": "is_attuned", visible: false}
            ],

        ajax: {

            url: 'http://localhost:8000/items/',
            "contentType": 'application/json',
            "headers": {
                'X-CSRFToken': csrftoken
            },
            "type": "POST",
            'mode': 'same-origin',
            "data": function (data, settings) {
                let js_data = JSON.stringify(data)
                // console.log(js_data)
                console.log(settings)
                return js_data
            },

            dataFilter: function (data) {
                let json = jQuery.parseJSON(data);
                json.recordsTotal = json.total;
                json.recordsFiltered = json.total
                let js_data = JSON.stringify(json)

                return js_data; // return JSON string
            },
        },
        createdRow: function (row) {
            let td = $(row).find(".truncate");
            td.attr("title", td.html());
        },
    });


    $('#table_id tbody').on('click', 'td.details-control', function () {
        let tr = $(this).closest('tr');
        let row = table.row(tr);
        let cell = $(tr).children("td").first()

        let i = cell.children()
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
            i.removeClass('fas fa-chevron-down')
            i.addClass('fas fa-chevron-right')

        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown')
            i.removeClass('fas fa-chevron-right')
            i.addClass('fas fa-chevron-down')
        }
    });
});


function call_backend() {
    fetch('http://localhost:8000/items')
        .then(response => response.json())
        .then(data => console.log(data));
}