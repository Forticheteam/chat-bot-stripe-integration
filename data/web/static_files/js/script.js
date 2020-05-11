// The max and min number of photos a customer can purchase
var MIN_PHOTOS = 1;
var MAX_PHOTOS = 10;
var sessionId = '';
var stripe = null;

var provincias = ['Alava','Albacete','Alicante','Almería','Asturias','Avila','Badajoz','Barcelona','Burgos','Cáceres',
'Cádiz','Cantabria','Castellón','Ciudad Real','Córdoba','A Coruña','Cuenca','Gerona','Granada','Guadalajara',
'Guipúzcoa','Huelva','Huesca','Islas Baleares','Jaén','León','Lérida','Lugo','Madrid','Málaga','Murcia','Navarra',
'Orense','Palencia','Las Palmas','Pontevedra','La Rioja','Salamanca','Segovia','Sevilla','Soria','Tarragona',
'Santa Cruz de Tenerife','Teruel','Toledo','Valencia','Valladolid','Vizcaya','Zamora','Zaragoza'];

$("#pay-button").text('Pagar €' + total + ' Ahora!');

var validateFields = function() {
  let valid = false;
  if (!protocolo || !name || !line_items) {
    alert("No se dispone de la información del Terapeuta, el protocolo o los productos");
    return;
  }
  $(".form-control").each(function(e, i) {
    if ($("#" + i.id).val()) {
      $("#" + i.id).addClass('is-valid');
      $("#" + i.id).removeClass('is-invalid');
      valid = true;
    } else {
      $("#" + i.id).addClass('is-invalid');
      valid = false;
    }
  });    
  if (!valid) {
    alert("Por favor completa todos los datos para poder Pagar!")
  } else {
    createCheckout();
  }
};


for(var i = 0; i < provincias.length; i++) {
    $('#select-provincia').append(`<option value="${provincias[i]}"> 
                                       ${provincias[i]} 
                                  </option>`); 
  } 

$("#pay-button").text('Pagar €' + total + ' Ahora!');
$("#pay-button").click(function () {
  validateFields();
});


// Create a Checkout Session with the selected quantity
var createCheckout = function () {
  return fetch('/create-checkout-session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      line_items: line_items,
      name: name,
      protocolo: protocolo,
      shipping_name: $("#name").val(),
      shipping_email: $("#email").val(),
      shipping_phone : $("#phone").val(),
      shipping_address: $("#address").val(),
      shipping_city: $("#city").val(),
      shipping_provincia: $("#select-provincia").val(),
      shipping_postalcode: $("#postalCode").val(),
      protocolo_id: $("#protocoloId").val(),
    }),
  }).then(function (result) {
    return result.json();
  })
  .then(function (json) {
    stripe
      .redirectToCheckout({
        sessionId: json.sessionId,
      })
      .then(handleResult);
    });
};

/* Get your Stripe publishable key to initialize Stripe.js */
fetch('/config')
  .then(function (result) {
    return result.json();
  })
  .then(function (json) {
    window.config = json;
    stripe = Stripe(config.publicKey);
  });
