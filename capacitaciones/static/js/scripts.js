// Al cargar la página, activar el Scrollspy
$('body').scrollspy({ target: '#list-videos' });

// Al hacer clic en un video, abrir el Modal correspondiente
$('#list-videos a').on('click', function(e) {
  e.preventDefault();
  var videoUrl = $(this).data('video-url');
  var videoTitle = $(this).text();
  $('#modal-video .modal-title').text(videoTitle);
  $('#modal-video .modal-body').html('<div class="embed-responsive embed-responsive-16by9"><iframe class="embed-responsive-item" src="' + videoUrl + '?autoplay=1" allowfullscreen></iframe></div>');
  $('#modal-video').modal('show');
});

// Al hacer clic en un botón de "Siguiente" o "Anterior", ir al video correspondiente
$('#modal-video').on('click', '.btn-next, .btn-prev', function() {
  var videoUrl = $(this).data('video-url');
  var videoTitle = $(this).data('video-title');
  $('#modal-video .modal-title').text(videoTitle);
  $('#modal-video .modal-body').html('<div class="embed-responsive embed-responsive-16by9"><iframe class="embed-responsive-item" src="' + videoUrl + '?autoplay=1" allowfullscreen></iframe></div>');
});
