// function for removing alert-info
window.setTimeout(function () {
    $(".alert").fadeTo(500, 0).slideUp(500, function () {
        $(this).remove();
    });
}, 3000);

// loading overlay on login-btn click
$('#login-btn').click(function () {
    $.LoadingOverlay("show", {
        color: "rgba(255, 255, 255, 0.8)",
        image: "/static/img/loading.gif",
        maxSize: "75px",
        minSize: "25px",
        resizeInterval: 0,
        size: "25%"
    });
});