// function for removing alert-info
window.setTimeout(function () {
    $(".alert").fadeTo(500, 0).slideUp(500, function () {
        $(this).remove();
    });
}, 3000);

function checkTextField(field) {
    if (field.value == '') {
        alert("Field is empty");
    }
}