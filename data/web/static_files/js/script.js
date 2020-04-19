// The max and min number of photos a customer can purchase
var MIN_PHOTOS = 1;
var MAX_PHOTOS = 10;

var provincias = ['Alava','Albacete','Alicante','Almería','Asturias','Avila','Badajoz','Barcelona','Burgos','Cáceres',
'Cádiz','Cantabria','Castellón','Ciudad Real','Córdoba','A Coruña','Cuenca','Gerona','Granada','Guadalajara',
'Guipúzcoa','Huelva','Huesca','Islas Baleares','Jaén','León','Lérida','Lugo','Madrid','Málaga','Murcia','Navarra',
'Orense','Palencia','Las Palmas','Pontevedra','La Rioja','Salamanca','Segovia','Sevilla','Soria','Tarragona',
'Santa Cruz de Tenerife','Teruel','Toledo','Valencia','Valladolid','Vizcaya','Zamora','Zaragoza'];

$("#pay-button").text('Pagar €' + total + ' Ahora!');

var validateFields = function() {
  let valid = false;
  $(".form-control").each(function(e, i) {
    console.log(e, i.id);
    console.log($("#" + i.id).val());
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
    createCheckoutSession();
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
var createCheckoutSession = function () {
  console.log(line_items);
  return;
  return fetch('/create-checkout-session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      line_items: line_items,
    }),
  }).then(function (result) {
    return result.json();
  });
};

/* Get your Stripe publishable key to initialize Stripe.js */
fetch('/config')
  .then(function (result) {
    return result.json();
  })
  .then(function (json) {
    window.config = json;
    var stripe = Stripe(config.publicKey);
    // Setup event handler to create a Checkout Session on submit
    document.querySelector('#submit').addEventListener('click', function (evt) {
      createCheckoutSession().then(function (data) {
        stripe
          .redirectToCheckout({
            sessionId: data.sessionId,
          })
          .then(handleResult);
      });
    });
  });
