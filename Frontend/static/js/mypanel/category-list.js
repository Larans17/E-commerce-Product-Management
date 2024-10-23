$(document).ready(function () {

    datatableList();

    // Clear Input Validation Messages
    $('input').on("click", function () {
        clearValidateMsg(this);
        $('#error_cate').text("")
    });

});

function formSubmit(form_id){
    showPreloader();
    let cate = $('#txtcategory').val();
    let form_data = $("#"+form_id).serialize();
    let isValid = Validate('categoryDiv');
    if(isValid == true){
        $.ajax({
            method: 'POST',
            url: '/create-category/',
            type: 'json',
            data:form_data
        }).done((data) => {
            
            if(data.status == 201){
                showMsg(data.message,1,5000);
                clearForm(form_id,'Category');
            }else{
                $('#txtcategory').val(cate);
                $('#error_cate').text(data.category_name[0]);
                $('#error_cate').addClass('error-text');
                
                if ($('#hd_cate_id').val()){
                    showMsg("Failed to updated",2,5000);
                }else{
                    showMsg("Failed to created",2,5000);
                }
            }
            hidePreloader();
            datatableList();
        })
    }
    hidePreloader();
}


function datatableList() {
    // Destroy existing DataTable instance if it exists
    if ($.fn.DataTable.isDataTable('#tblCategoryList')) {
        $('#tblCategoryList').DataTable().destroy();
    }

    // Initialize DataTable
    dataTable = $('#tblCategoryList').DataTable({
        responsive: true,
        autoWidth: false,
        columnDefs: [
            {
                className: 'dt-body-center text-center',
                targets: [0, 3],
                orderable: false,
            },
        ],
        "aLengthMenu": [
            [10, 30, 50, -1],
            [10, 30, 50, "All"]
        ],
        "oLanguage": dataTabledictionary,
        "iDisplayLength": 10,
        processing: true,
        serverSide: true,
        serverMethod: 'GET',
        "ajax": {
            "url": "/category-list-datatable/",
            'data': function (data) {
            },
        },
        'columns': [
            {
                "data": null, 'width': 20, "orderable": false, render: function (data, type, row, meta) {
                    count = (meta.row + 1) + (meta.settings._iDisplayStart)
                    return count
                }
            },
            {
                "data": null, 'width': 50, "class": "text-left", render: function (data) {
                    return (data.category_name != '') ? data.category_name : '-';
                }
            },
            {
                "data": null, 'width': 50, "class": "text-center", render: function (data) {
                    // Add logic for rendering data in this column
                    return (data.edited_date != null) ? data.edited_date : data.created_date;
                }
            },
            {
                "data": null,
                "width": 50,
                "class": "text-center",
                "render": function (data) {
                    // Add logic for rendering data in this column
                    return `
                    <div class="flex align-items-center list-user-action">
                    <a class="btn btn-sm bg-success" data-toggle="tooltip" data-placement="top" title="" data-original-title="Edit" href="#" onclick="EditRow('${data.id}')"><i class="ri-pencil-line mr-0"></i></a>
                     <a class="btn btn-sm bg-danger" data-toggle="tooltip" data-placement="top" title="" data-original-title="Delete" onclick="confirmDeleteModal('href','/delete-category/?category_id=${data.id}')"><i class="ri-delete-bin-line mr-0"></i></a>
                  </div>
                  `;
                }
            }
        ],
        initComplete: function () {
            // Call your function here
            $('[data-toggle="tooltip"]').tooltip();
        }
    });
}



// Edit Functions
function EditRow(categoryid) {
    clearFormError('category_form');
    showPreloader();
    $.ajax({
        url: `/get-category/?category_id=${categoryid}`,
        data: '',
        success: function (data) {
            console.log(data)
        },
        error: function () {
            showMsg('something went wrong',2,5000)
        }
    }).done(function (data) {
        hidePreloader();

        $('#txtcategory').val(data.category_name).focus()
        $('#hd_cate_id').val(data.id);
        $('#titleName').text('Edit Category');
        $('#btnSave').text('Update Category');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    })
}