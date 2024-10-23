$(document).ready(function () {
  var activeUrl = $('[href="' + currentUrl + '"]');
  if (activeUrl.length !== 0) {
    activeUrl.parent().addClass("active");
    if (activeUrl.closest('.iq-submenu').length) {
      activeUrl.closest('.iq-submenu').addClass('show');
      activeUrl.closest('.iq-submenu').parent().addClass('active');
    }
  }
});

// For Remove Content from datatables

var dataTabledictionary = {
  sLengthMenu: "_MENU_",
  sInfo: "_START_ to _END_ of _TOTAL_",
  sInfoEmpty: "0 to 0 of 0",
  sInfoFiltered: "(filtered from _MAX_ total records)",
  sSearchPlaceholder: "Search...",
  sSearch: "",
};

// ********* func for an Form Validations ***********

function Validate(divId) {
  var result = true;
  $("#" + divId + " :input").each(function (n, element) {
    var validateAttr = $(this).attr("validate");
    var elementId = $(this).attr("id");
    var dataName = $(this).attr("data-name");
    $(this).nextAll(".error-text").remove();

    if (
      typeof validateAttr !== "undefined" &&
      validateAttr !== false &&
      ($.trim($(element).val()) == "" || $.trim($(element).val()) == "0")
    ) {
      //-----------select-----------
      if ($(element).is("select")) {
        $("#" + elementId).addClass("form-error");
        $("#select2-" + elementId + "-container").addClass("form-error");
        $(this)
          .parent()
          .append(
            "<span class='error-text'>" +
              `Please select any one ${dataName}` +
              "</span>"
          );
        result = false;
      }
      //-----------input-----------
      else {
        if ($.trim($(element).val()).length <= 0) {
          if ($(this).parent().hasClass("input-group")) {
            $(this).parent().nextAll(".error-text").remove();
            $(this)
              .parent()
              .parent()
              .append(
                "<span class='error-text'>" +
                  `${dataName} should not be empty` +
                  "</span>"
              );
            $(this).addClass("form-error");
          } else {
            $(this)
              .parent()
              .append(
                "<span class='error-text'>" +
                  `${dataName} should not be empty` +
                  "</span>"
              );
            $(this).addClass("form-error");
          }
          result = false;
        }
      }
    } else {
      if ($("#" + elementId).val() == "" && $("#" + elementId).val() == "0") {
        $(this).nextAll(".error-text").remove();
        if (
          $(element).is("select") &&
          ($.trim($(element).val()) == "" || $.trim($(element).val()) == "0")
        ) {
          $("#" + elementId).removeClass("form-error");
          result = false;
        } else {
          $(this).removeClass("form-error");
          result = false;
        }
      }
    }
  });

  $("#" + divId + " :input").each(function (n, element) {
    var validateAttr = $(this).attr("validate");
    var ElementId = $(this).attr("id");
    if (
      typeof validateAttr !== "undefined" &&
      validateAttr !== false &&
      ($.trim($(element).val()) == "" || $.trim($(element).val()) == "0") &&
      $.trim($(element).val()).length == 0
    ) {
      $("#" + ElementId).focus();
      return false;
    }
  });
  return result;
}

// ********* func for an Form Clear Validation ***********
function clearValidateMsg(element) {
  var elementId = $(element).attr("id");
  if (
    $("#" + elementId)
      .parent()
      .hasClass("input-group")
  ) {
    $("#" + elementId)
      .parent()
      .parent()
      .find("span.error-text")
      .remove();
    $("#" + elementId)
      .parent()
      .parent()
      .find(".form-error")
      .removeClass("form-error");
  } else {
    $("#" + elementId)
      .parent()
      .find("span.error-text")
      .remove();
    $("#" + elementId)
      .parent()
      .find(".form-error")
      .removeClass("form-error");
  }
}

// ********* func for an Form Clear ***********
$.fn.clearForm = function () {
  return this.each(function () {
    $(":input", this).each(function () {
      var type = this.type,
        tag = this.tagName.toLowerCase();
      if (
        !$(this).attr("readonly") &&
        (type == "text" ||
          type == "password" ||
          tag == "textarea" ||
          type == "email")
      ) {
        if ($(this).attr("control") == "date") {
          this.value = GetTodayDate("/");
        } else if ($(this).attr("control") == "time") {
          var now = new Date();
          var time = now.format("h:i A");
          this.value = time;
        } else this.value = "";
      } else if (tag == "select") {
        this.selectedIndex = 0;
        $(this).val("0").trigger("change");
      } else if (type == "checkbox") {
        $(this).prop("checked", false);
      }
    });

    // Remove validation error messages and control border colors
    $(this).find("span.error-text").remove();
    $(this).find(".form-error").removeClass("form-error");
  });
};



function clearForm(id,name){
  $("#"+id)[0].reset();
  $('#titleName').text('Add'+' ' + name);
  $('#btnSave').text('Add'+' ' + name);
  if (name == 'Category'){
    $('#hd_cate_id').val("");

  }else if(name == 'Product'){
    $('#hd_subcate_id').val("");
    $('#txtcategory').val("");
    $('#ddlcategory').val('0').trigger('change');

  }else{

  }
  clearFormError(id);
}



// clear form error message 

function clearFormError(id){
  var error_class_list = $("#"+id).find('.form-error');
    $.each(error_class_list,function(idx,val){
        $(val).removeClass('form-error')
    })
    var error_text_list = $("#"+id).find('.error-text');
    $.each(error_text_list,function(idx,val){
        $(val).html('');
    })
}


// ---func for an using delete popup model------->>
function confirmDeleteModal(attr, next_step, content = null) {
  var modal_id = $("#modalDelete");
  var modal_content = modal_id.find("#modal_content");
  var modal_button = modal_id.find("#comfirmModalDelete");
  if (content) {
    modal_content.html(content);
  } else {
    modal_content.html("Are You Sure?");
  }

  if (modal_button.attr("href") !== undefined) {
    modal_button.removeAttr("href");
  }

  if (modal_button.attr("onclick") !== undefined) {
    modal_button.removeAttr("onclick");
  }
  modal_button.attr(attr, next_step);
  modal_id.modal("show");
}

function valueAgainstTriggerFun(id, optionVal) {
  var select2 = $("#" + id);
  var option = select2.find('option:contains("' + optionVal + '")');
  option.prop("selected", true);
  select2.trigger("change");
  return;
}


function showPreloader(){
  $('#preloader').css({'display':''})
}

function hidePreloader(){
  $('#preloader').css({'display':'none'})
}



