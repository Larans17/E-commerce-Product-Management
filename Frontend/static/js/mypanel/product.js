let searchKey = "";
let pageCount = 1;
let totalPages = 1;

$(document).ready(function() {
    productPagination(pageCount);

    $("#searchkey").keyup(function() {
        searchKey = $(this).val();
        pageCount = 1; // Reset to first page on new search
        productPagination(pageCount);
    });

});

function productPagination(page) {
    
    return $.ajax({
        url: "/search-related-product/",
        data: {
            page: page,
            searchword: searchKey,
        },
        dataType: "json",
        success: function(data) {
            totalPages = data.total_pages;
            $("#product_result_block").html(''); // Clear previous results

            if (data.count > 0) {
                data.results.products.forEach(product => {
                    $("#product_result_block").append(renderProductCard(product));
                });
                renderPagination(page, totalPages);
            } else {
                $("#searchbar_empty_block").html(`<div class="text-center mb-10 mt-10"><h1 class="text-muted">Product not found.</h1></div>`);
                $("#product_footer_block").html("");
            }
        },
        error: function() {
            console.error("Error loading products");
        },
        complete: function() {
        }
    });
}

function renderPagination(currentPage, totalPages) {
    let paginationHtml = '';
    
    // Previous button
    if (currentPage > 1) {
        paginationHtml += `<li class="page-item"><a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a></li>`;
    }

    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === currentPage) {
            paginationHtml += `<li class="page-item active"><a class="page-link" href="#">${i}</a></li>`;
        } else {
            paginationHtml += `<li class="page-item"><a class="page-link" href="#" data-page="${i}">${i}</a></li>`;
        }
    }

    // Next button
    if (currentPage < totalPages) {
        paginationHtml += `<li class="page-item"><a class="page-link" href="#" data-page="${currentPage + 1}">Next</a></li>`;
    }

    $("#pagination").html(paginationHtml);

    // Add click event for pagination links
    $(".page-link").click(function(e) {
        e.preventDefault();
        const page = $(this).data("page");
        if (page) {
            pageCount = page; // Update the current page
            productPagination(pageCount); // Fetch the new page
        }
    });
}

function renderProductCard(product) {
    return `
      <div class="col">
        <div class="card card-product">
          <div class="card-body">
            <div class="text-small mb-1">
              <a href="#" class="text-decoration-none text-muted"><small>${product.category_name}</small></a>
            </div>
            <h2 class="fs-6 mb-0">${product.product_name}</h2>
            <p>${product.description}</p>
            <div class="d-flex justify-content-between align-items-center mt-3">
              <span class="text-dark">₹ ${product.price}</span>
            </div>
          </div>
        </div>
      </div>`;
}
