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
});
