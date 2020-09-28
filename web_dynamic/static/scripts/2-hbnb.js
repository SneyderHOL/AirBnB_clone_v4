const $ = window.$;
$(document).ready(function () {
  var objs = {};
  $('input').change(function () {
    if ($(this).is(':checked')) {
      objs[$(this).attr('data-name')] = $(this).attr('data-id');
    } else if ($(this).is(':not(:checked)')) {
      delete objs[$(this).attr('data-name')];
    }
    const names = Object.keys(objs);
    $('.amenities h4').text(names.sort().join(', '));
  });

  $.get('http://0.0.0.0:5001/api/v1/status', function (data) {
    console.log(data.status);
    if (data.status === 'OK') {
      $('#api_status').css('background-color', '');
      $('#api_status').addClass('available');
    }
  });
});
