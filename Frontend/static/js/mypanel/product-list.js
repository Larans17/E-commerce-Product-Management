$(document).ready(function () {
    dataTableList();

    $("#ddlcategory").select2({
        tags: true,
        placeholder: "Search and add",
    });


 // Clear Input Validation Mesages
 $('input').on("click", function () {
    clearValidateMsg(this);
    $('#error_product_name').text("")
});
$('textarea').on("click", function () {
    clearValidateMsg(this);
});
$('select').on("change", function () {
    clearValidateMsg(this);
  });




});



function formSubmit(form_id){
showPreloader();
let cate = $('#ddlcategory').val();
let price = $('#txt_price').val();
let desc = $('#txtdesc').val();
let product_name = $('#txt_product_name').val();

let form_data = $("#"+form_id).serialize();
let isValid = Validate('productDiv');
if(isValid == true){
    $.ajax({
        method: 'POST',
        url: '/create-product/',
        type: 'json',
        data:form_data,
    }).done((data) => {
        if(data.status == 201){
            showMsg(data.message,1,5000);
            clearForm(form_id,'Product');
            dataTable.draw();
            $("#" + form_id + " select").val('0').trigger('change');
        }else{
            console.log(data);
            
            $('#ddlcategory').val(cate).trigger('change');
            $('#txt_price').val(price);
            $('#txtdesc').val(desc);
            $('#txt_product_name').val(product_name);
            $('#error_product_name').text(data.product_name[0]);
            $('#error_product_name').addClass('error-text');

            if ($('#hd_procut_id').val()){
                showMsg("Failed to updated",2,5000);
            }else{
                showMsg("Failed to created",2,5000);
            }
        }
        
    })
}
hidePreloader();
}



// DATATABLES ::

function dataTableList() {
// Destroy existing DataTable instance if it exists
if ($.fn.DataTable.isDataTable('#tblProductList')) {
    $('#tblProductList').DataTable().destroy();
}

// Initialize DataTable
dataTable = $('#tblProductList').DataTable({
    responsive: true,
    autoWidth: false,
    columnDefs: [
        {
            className: 'dt-body-center text-center',
            targets: [0, 6],
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
        "url": "/product-list-datatable/",
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
            "data": null, 'width': 80, "class": "text-center", render: function (data) {
                list = ""
                if (data.created_date != ''){
                    list = `
                    <span class="">${data.created_date}</span>`
                }else{
                    list = `-`
                }
                return list
            }
        },
        {
            "data": null, 'width': 50, "class": "text-left", render: function (data) {
                return (data.category_name != '') ? data.category_name : '-';
            }
        },
        
        {
            "data": null, 'width': 50, "class": "text-left", render: function (data) {
                return (data.product_name != '') ? data.product_name : '-';
            }
        },
        {
            "data": null, 'width': 50, "class": "text-left", render: function (data) {
                return (data.price != '') ? '₹ '+data.price : '-';
            }
        },
        {
            "data": null, 'width': 50, "class": "text-left", render: function (data) {
                return (data.description != '') ? data.description : '-';
            }
        },
        {
            "data": null,
            "width": 50,
            "class": "text-center",
            "render": function (data) {
                return `
                <div class="flex align-items-center list-user-action">
                <a class="btn btn-sm bg-success" data-toggle="tooltip" data-placement="top" title="" data-original-title="Edit" href="#" onclick="EditRow('${data.id}')"><i class="ri-pencil-line mr-0"></i></a>
                 <a class="btn btn-sm bg-danger" data-toggle="tooltip" data-placement="top" title="" data-original-title="Delete" href="#" onclick="confirmDeleteModal('href','/delete-product/?product_id=${data.id}')"><i class="ri-delete-bin-line mr-0"></i></a>
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
function EditRow(product_id) {
    showPreloader();
$.ajax({
    url: `/get-product/?product_id=${product_id}`,
    data: '',
    success: function (data) {
    },
    error: function () {
        showMsg('something went wrong',2,5000)
    }
}).done(function (data) {
    $('#ddlcategory').val(data.category).trigger('change').focus();
    $('#titleName').text('Edit Product');
    $('#btnSave').text('Update Product');
    $('#txt_price').val(data.price);
    $('#txtdesc').val(data.description);
    $('#txt_product_name').val(data.product_name);
    $('#hd_product_id').val(data.id);
    
})
hidePreloader();
}





  