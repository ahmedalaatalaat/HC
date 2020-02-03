var phone_no = 0;
var address_no = 0;
var relatives_phone_no = 0;
$('#add_form').submit(function (e) {
    e.preventDefault();
    if($('#txtPwd').val() == $('#txtConfirmPwd').val()){
        var input_data = new FormData(this);
        $.ajax({
        method: 'POST',
        url: window.location.href,
        data: input_data,
        contentType: false,
        processData: false,
        success: function (data) {
            $.growl.notice({ title: "Add Notice", message: "New data has been added successfully" });
            document.getElementById("add_form").reset();
            $('#password_main').html('Password');
            $('#password_Confirm').html('Confirm Password');
            $('#switch-8').removeAttr("checked");
            $('#switch_label').attr("class", 'mdl-switch mdl-js-switch mdl-js-ripple-effect mdl-js-ripple-effect--ignore-events is-upgraded');
            $('#image_placeholder').html('<i class="fa fa-file-image-o"></i>');
            $('#image_text').html('Drag&amp;Drop files here');
        },
        error: function (error_data) {
            if(error_data.responseText == 'This doctor data is already stored'){
                var message = error_data.responseText
            }
            else{
                var message = "New data faild to be added";
            }
            console.log(error_data.responseText);
            $.growl.error({ title: "Error Notice",message:message});
        }
    });
    }
    else{
        $.growl.error({ title: "Password Error",message: "Password is not matched" });
        $('#password_main').html('<font color="red">Password is not matched</p>');
        $('#password_Confirm').html('<font color="red">Password is not matched</p>');
        $('#password_main_div').attr('class',"mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width is-upgraded");
        $('#password_confirm_div').attr('class',"mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width is-upgraded");
        $('#txtPwd').val(null);
        $('#txtConfirmPwd').val(null);
    }

});
$('#add_form_Cancel_button').click(function(){
    document.getElementById("add_form").reset();
    $('#password_main').html('Password');
    $('#password_Confirm').html('Confirm Password');
    $('#switch-8').removeAttr("checked");
    $('#switch_label').attr("class", 'mdl-switch mdl-js-switch mdl-js-ripple-effect mdl-js-ripple-effect--ignore-events is-upgraded');
    $('#image_placeholder').html('<i class="fa fa-file-image-o"></i>');
    $('#image_text').html('Drag&amp;Drop image here');
});

function image_upload(){
    $('#image_placeholder').html('<i class="fa fa-check-circle-o" style="color: green"></i>');
    $('#image_text').html('Upload another image');
}

function phone_add(){
    phone_no += 1
    $('#Phone').append(`
    <div id="phone_`+ phone_no +`">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
            <input class="mdl-textfield__input" id="text5" pattern="-?[0-9]*(\.[0-9]+)?" type="text" name="Phone" placeholder="Mobile Number"/>
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
            <button class = "btn btn-pinterest waves-effect waves-light" type = "button" onclick = "phone_delete(`+ phone_no +`)">
                <i class="fa fa-trash-o"></i>
            </button>
        </div>
    </div>`);
}

function phone_delete(num){
    $('#phone_' + num).remove();
}

function relatives_phone_add(){
    relatives_phone_no += 1
    $('#relatives_Phone').append(`
    <div id="relatives_phone_`+ relatives_phone_no +`">
        <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
            <input class="mdl-textfield__input" id="text5" pattern="-?[0-9]*(\.[0-9]+)?" type="text" name="relatives_phones" placeholder="Relatives Phone Number"/>
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
            <button class = "btn btn-pinterest waves-effect waves-light" type = "button" onclick = "relatives_phone_delete(`+ relatives_phone_no +`)">
                <i class="fa fa-trash-o"></i>
            </button>
        </div>
    </div>`);
}

function relatives_phone_delete(num){
    $('#relatives_phone_' + num).remove();
}

function address_add(){
    address_no += 1;
    $('#Address').append(`
        <div id="address_`+ address_no +`">
            <div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width">
                <input class="mdl-textfield__input" type="text" name="address" placeholder="Address" />
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
                <button class = "btn btn-pinterest waves-effect waves-light" type = "button" onclick = "address_delete(`+ address_no +`)">
                <i class="fa fa-trash-o"></i>
            </button>
            </div>
        </div>`);
}

function address_delete(num){
    $('#address_' + num).remove();
}

function date_val(){
    if ($('#dp1').val() != ""){
        $('#date_add').attr('class', 'mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width is-dirty');
    }

}

function datetime_val(){
    if($('#datetime_add').val != ""){
        $('#datetime_add').attr('class', 'mdl-textfield mdl-js-textfield mdl-textfield--floating-label txt-full-width is-dirty');
    }
}

// $('#my-select').multiSelect();
