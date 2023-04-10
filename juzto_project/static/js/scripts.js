$(document).ready(function () {
    //jquery para los submenús
    $('.sub-btn').click(function () {
        $(this).next('.sub-menu').slideToggle();
        $(this).find('dropdown').toggleClass('rotate');
    });

    //jquery para el boton de menú sidebar
    $('.menu-btn').click(function () {
        $('.side-bar').addClass('active');
        $('.menu-btn').css("visibility", "visible");
    });

    $('.close-btn').click(function () {
        $('.side-bar').removeClass('active');
        $('.menu-btn').css("visibility", "hidden");                
    });
});