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

  $.ajax({
    url: 'http://0.0.0.0:5001/api/v1/places_search',
    type: 'POST',
    success: function (data) {
      const resultSize = data.length;
      if (resultSize === 0) {
        console.log('No data found');
        return;
      }
      for (let i = 0; i < resultSize; i++) {
        let guestPluralString = '';
        const maxGuest = data[i].max_guest;
        if (maxGuest > 1) {
          guestPluralString = 's';
        }
        let roomPluralString = '';
        const numberRooms = data[i].number_rooms;
        if (numberRooms > 1) {
          roomPluralString = 's';
        }
        let bathroomPluralString = '';
        const numberBathrooms = data[i].number_bathrooms;
        if (numberBathrooms > 1) {
          bathroomPluralString = 's';
        }
        $('.places').append(
          '<article>\
             <div class="title_box">\
               <h2>' + data[i].name + '</h2>\
               <div class="price_by_night">' + '$' + data[i].price_by_night + '</div>\
             </div>\
           <div class="information">\
             <div class="max_guest">' + maxGuest + ' Guest' + guestPluralString + '</div>\
             <div class="number_rooms">' + numberRooms + ' Bedroom' + roomPluralString + '</div>\
             <div class="number_bathrooms">' + numberBathrooms + ' Bathroom' + bathroomPluralString + '</div>\
           </div>\
           <div class="description">' + data[i].description + '</div>\
           </article>');
      }
    },
    data: JSON.stringify({}),
    headers: { 'Content-Type': 'application/json' }
  });
});
