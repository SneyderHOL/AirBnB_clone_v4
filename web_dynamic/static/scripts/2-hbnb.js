$(document).ready(function () {
  $.get('http://0.0.0.0:5001/api/v1/status', function (data) {
    console.log(data.status);
    if (data.status == 'OK') {
      $('#api_status').css('background-color', '');
      $('#api_status').addClass('available');
    };
  });
});
