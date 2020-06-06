$('#ai_form').submit(function(e) {
    e.preventDefault();
    $.ajax({
        method: 'POST',
        url: window.location.href,
        data: new FormData(this),
        contentType: false,
        processData: false,
        success: function(data) {
            $('#modal_data').html(data.result);
            $('#ai_results_modal').modal('show');
        },
        error: function(error_data) {
            $.growl.error({ title: "Error Notice", message: message });
        }
    });
});

$('#ai_form_Cancel_button').click(function() {
    document.getElementById("ai_form").reset();
    $('#image_placeholder').html('<i class="fa fa-file-image-o"></i>');
    $('#image_text').html('Drag&amp;Drop image here');
});
