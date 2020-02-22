var phone_no = 0;
var address_no = 0;
var relatives_phone_no = 0;
var specialization_no = 0;
var analysis_and_radiology_no = 0;
$('#add_form').submit(function(e) {
    e.preventDefault();
    if ($('#txtPwd').val() == $('#txtConfirmPwd').val()) {
        var input_data = new FormData(this);
        $.ajax({
            method: 'POST',
            url: window.location.href,
            data: input_data,
            contentType: false,
            processData: false,
            success: function(data) {
                $.growl.notice({ title: "Add Notice", message: "New data has been added successfully" });
                if (!(($('.page-title').html()).includes('Edit'))) {
                    document.getElementById("add_form").reset();
                    $('#password_main').html('Password');
                    $('#password_Confirm').html('Confirm Password');
                    $('#switch-8').removeAttr("checked");
                    $('#switch_label').attr("class", 'mdl-switch mdl-js-switch mdl-js-ripple-effect mdl-js-ripple-effect--ignore-events is-upgraded');
                    $('#image_placeholder').html('<i class="fa fa-file-image-o"></i>');
                    $('#image_text').html('Drag&amp;Drop files here');
                }
            },
            error: function(error_data) {
                if (error_data.responseText.includes('already stored')) {
                    var message = error_data.responseText
                } else {
                    var message = "New data faild to be added";
                }
                console.log(error_data.responseText);
                $.growl.error({ title: "Error Notice", message: message });
            }
        });
    } else {
        $.growl.error({ title: "Password Error", message: "Password is not matched" });
        $('#password_main').html('<font color="red">Password is not matched</p>');
        $('#password_Confirm').html('<font color="red">Password is not matched</p>');
        $('#password_main_div').attr('class', "mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width is-upgraded");
        $('#password_confirm_div').attr('class', "mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width is-upgraded");
        $('#txtPwd').val(null);
        $('#txtConfirmPwd').val(null);
    }

});
$('#add_form_Cancel_button').click(function() {
    document.getElementById("add_form").reset();
    $('#password_main').html('Password');
    $('#password_Confirm').html('Confirm Password');
    $('#switch-8').removeAttr("checked");
    $('#switch_label').attr("class", 'mdl-switch mdl-js-switch mdl-js-ripple-effect mdl-js-ripple-effect--ignore-events is-upgraded');
    $('#image_placeholder').html('<i class="fa fa-file-image-o"></i>');
    $('#image_text').html('Drag&amp;Drop image here');
});

function image_upload() {
    $('#image_placeholder').html('<i class="fa fa-check-circle-o" style="color: green"></i>');
    $('#image_text').html('Upload another image');
}

function phone_add() {
    phone_no += 1
    $('#phone').append(`
    <div id="phone_` + phone_no + `">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
            <input class="mdl-textfield__input" id="text5" pattern="-?[0-9]*(\.[0-9]+)?" type="text" name="phone" placeholder="Mobile Number" required autocomplete="nope"/>
            <label class="mdl-textfield__label" for="text5">
            </label>
            <span class="mdl-textfield__error">
                Number required!
            </span>
        </div>
        <div align = "right">
            <button class="btn btn-skype waves-effect waves-light" type="button" onclick="phone_add()">
                <i class="fa fa-plus"></i>
            </button>
            <button class = "btn btn-pinterest waves-effect waves-light" type = "button" onclick = "phone_delete(` + phone_no + `)">
                <i class="fa fa-trash-o"></i>
            </button>
        </div>
    </div>`);
}

function phone_delete(num) {
    $('#phone_' + num).remove();
}

function relatives_phone_add() {
    relatives_phone_no += 1
    $('#relatives_phone').append(`
    <div id="relatives_phone_` + relatives_phone_no + `">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
            <input class="mdl-textfield__input" id="text5" pattern="-?[0-9]*(\.[0-9]+)?" type="text" name="relatives_phones" placeholder="Relatives phone Number" required autocomplete="nope"/>
            <label class="mdl-textfield__label" for="text5">
            </label>
            <span class="mdl-textfield__error">
                Number required!
            </span>
        </div>
        <div align = "right">
            <button class="btn btn-skype waves-effect waves-light" type="button" onclick="relatives_phone_add()">
                <i class="fa fa-plus"></i>
            </button>
            <button class = "btn btn-pinterest waves-effect waves-light" type = "button" onclick = "relatives_phone_delete(` + relatives_phone_no + `)">
                <i class="fa fa-trash-o"></i>
            </button>
        </div>
    </div>`);
}

function relatives_phone_delete(num) {
    $('#relatives_phone_' + num).remove();
}

function address_add() {
    address_no += 1;
    $('#Address').append(`
        <div id="address_` + address_no + `">
            <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
                <input class="mdl-textfield__input" type="text" name="address" placeholder="Address" required autocomplete="nope"/>
                <label class="mdl-textfield__label">
                </label>
                <span class="mdl-textfield__error">
                    Address required!
                </span>
            </div>
            <div align="right">
                <button class="btn btn-skype waves-effect waves-light" type="button" onclick="address_add()">
                    <i class="fa fa-plus"></i>
                </button>
                <button class = "btn btn-pinterest waves-effect waves-light" type = "button" onclick = "address_delete(` + address_no + `)">
                <i class="fa fa-trash-o"></i>
                </button>
            </div>
        </div>`);
}

function address_delete(num) {
    $('#address_' + num).remove();
}

function date_val() {
    if ($('#dp1').val() != "") {
        $('#date_add').attr('class', 'mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width is-dirty');
    }

}

function datetime_val() {
    if ($('#datetime_add').val != "") {
        $('#datetime_add').attr('class', 'mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width is-dirty');
    }
}

MaterialTextfield.prototype.checkValidity = function() {
    var CLASS_VALIDITY_INIT = "validity-init";
    if (this.input_ && this.input_.validity && this.input_.validity.valid) {
        this.element_.classList.remove(this.CssClasses_.IS_INVALID);
    } else {

        if (this.input_ && this.input_.value.length > 0) {
            this.element_.classList.add(this.CssClasses_.IS_INVALID);
        } else if (this.input_ && this.input_.value.length === 0) {
            if (this.input_.classList.contains(CLASS_VALIDITY_INIT)) {
                this.element_.classList.add(this.CssClasses_.IS_INVALID);
            }
        }


    }

    if (this.input_.length && !this.input_.classList.contains(CLASS_VALIDITY_INIT)) {
        this.input_.classList.add(CLASS_VALIDITY_INIT);
    }
};

function delete_item(id) {
    swal({
        title: "Are you sure?",
        text: "Do you want to delete " + id,
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#dc3545",
        confirmButtonText: "Yes, delete it!",
        closeOnConfirm: false
    }, function() {
        $.ajax({
            method: 'POST',
            url: window.location.href,
            data: {
                id: id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                $('#' + id).remove();
                swal("Deleted!", id + " has been deleted.", "success");
            }
        });

    });
}

function delete_model() {
    $("#Deleteitem").modal();
}


function specialization_add() {
    specialization_no += 1;
    $('#Specializations').append(`
        <div id="specialization_` + specialization_no + `">
            <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
                <input class="mdl-textfield__input" type="text" name="specialization" placeholder="Specialization" autocomplete="nope" required/>
                <label class="mdl-textfield__label">
                </label>
            </div>
            <div align="right">
                <button class="btn btn-skype waves-effect waves-light" type="button" onclick="specialization_add()">
                    <i class="fa fa-plus">
                    </i>
                </button>
                <button class = "btn btn-pinterest waves-effect waves-light" type = "button" onclick = "specialization_delete(` + specialization_no + `)">
                    <i class="fa fa-trash-o"></i>
                </button>
            </div>
        </div>`);
}

function specialization_delete(num) {
    $('#specialization_' + num).remove();
}


function analysis_and_radiology_add(){
    analysis_and_radiology_no += 1;
    $('#Analysis_and_Radiology').append(`
        <div id="analysis_and_radiology_` + analysis_and_radiology_no + `">
            <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
                <input class="mdl-textfield__input" id="text_analysis_and_radiology" maxlength="25" required type="text" name="analysis_and_radiology" autocomplete="no" placeholder="Analysis And Radiology"/>
                <label class="mdl-textfield__label" for="text_analysis_and_radiology">
                </label>
                <span class="mdl-textfield__error">
                    Analysis And Radiology required!
                </span>
            </div>
            <div align="right">
                <button class="btn btn-skype waves-effect waves-light" type="button" onclick="analysis_and_radiology_add()">
                    <i class="fa fa-plus">
                    </i>
                </button>
                <button class = "btn btn-pinterest waves-effect waves-light" type = "button" onclick = "analysis_and_radiology_delete(` + analysis_and_radiology_no + `)">
                <i class="fa fa-trash-o"></i>
                </button>
            </div>
        </div>
        `);
}

function analysis_and_radiology_delete(num) {
    $('#analysis_and_radiology_' + num).remove();
}
