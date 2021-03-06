function format(row_data) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Full Description:</td>' +
        '<td>' + row_data.text_description.replace(/(?:\r\n|\r|\n)/g, '<br>') + '</td>' +
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
        autoWidth: false,
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
                    "data": null,
                    "className": "row-command",
                    "orderable": false,
                    "ordering": false,
                    "render": function (data, type, row, meta) {
                        let id = row.id
                        let view_link = `${BACKEND_POST_URL}${row.model_name}/${id}`
                        let edit_link = `${ITEM_ADMIN_ROOT}${row.model_name}/${id}/change`

                        console.log(view_link)
                        let view_link_display = `<a href=${view_link}><i class="far fa-eye"></i></a>`
                        let edit_link_display = `<a href=${edit_link}><i class="far fa-edit"></i></a>`
                        return `${view_link_display} <span style="padding-left: 3px"></span>${edit_link_display}`
                    },
                },
                {"data": "name", "className": "name_column"},
                {"data": "text_description", visible: false},
                {"data": "rarity", visible: false},
                {
                    "data": "requires_attunement", "className": "attunement_col icon",
                    "render": function (data, type, row, meta) {
                        let requires = data
                        let attuned = row.is_attuned

                        let placeholder

                        if (requires && attuned) {
                            placeholder = "<i class='fas fa-lock attuned'/>"
                        } else if (requires) {
                            placeholder = '<i class="fas fa-lock-open unattuned"/>'
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

            url: BACKEND_POST_URL,
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
