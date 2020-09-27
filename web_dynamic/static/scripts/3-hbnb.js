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

  $.post('http://0.0.0.0:5001/api/v1/places_search', function (data, textStatus, typeResponse) {
    console.log(typeResponse);
    if (typeResponse !== 'json') {
      console.log('Wrong type of result');
      return;
    }
    const resultSize = data.length;
    console.log(resultSize);
    if (resultSize === 0) {
      console.log('No data found');
      return;
    }
    // for (let i = 0; i < 1; i++) {
    for (let i = 0; i < resultSize; i++) {
      if (data[i].__class__ !== 'Place') {
        console.log('No place');
        continue;
      }
      $('<article></article>').appendTo('.places');
      $('<div class="title_box"></div>').appendTo('.places article');
      $('<h2>' + data[i].name + '</h2>').appendTo('.places article .title_box');
      $('<div class="price_by_night">' + data[i].price_by_night + '</div>').appendTo('.places article .title_box');
      $('<div class="information"></div>').appendTo('.places article');
      const maxGuest = data[i].max_guest;
      let pluralString = '';
      if (maxGuest > 1) {
        pluralString = 's';
      }
      $('<div class="max_guest">' + maxGuest + ' Guest' + pluralString + '</div>').appendTo('.places article .information');
      pluralString = '';
      const numberRooms = data[i].number_rooms;
      if (numberRooms > 1) {
        pluralString = 's';
      }
      $('<div class="number_rooms">' + numberRooms + ' Bedroom' + pluralString + '</div>').appendTo('.places article .information');
      pluralString = '';
      const numberBathrooms = data[i].number_bathrooms;
      if (numberBathrooms > 1) {
        pluralString = 's';
      }
      $('<div class="number_bathrooms">' + numberBathrooms + ' Bathroom' + pluralString + '</div>').appendTo('.places article .information');
      $('<div class="description">' + data[i].description + '</div>').appendTo('.places article');
    }
  });
});
