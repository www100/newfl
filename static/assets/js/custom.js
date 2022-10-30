let strlist = "";
//add items to the string then convert to json obj
for (let index = 0; index < countriesPT.length; index++) {
strlist = strlist + `"${countriesPT[index].flag}":"${countriesPT[index].namePt}",`
}
strlist = strlist.slice(0, -1); 
const myobj = JSON.parse('{'+strlist+'}')

// Set the input ID and select it
var input = document.querySelector("#phone");
// initialise plugin
var iti = window.intlTelInput(input, {
initialCountry: "BR",
localizedCountries: myobj,
nationalMode: true,
utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.19/js/utils.js"
});

iti.getNumber();


const stripe = Stripe('{{STRIPE_PKEY}}');
const options = {
clientSecret: '{{CLIENT_SECRET}}',
// Fully customizable with appearance API.
appearance: {
theme: 'stripe'
},
};

// Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 3
const elements = stripe.elements(options);

// Create and mount the Payment Element
const paymentElement = elements.create('payment', {
layout: {
type: 'tabs',
defaultCollapsed: false,
}
});
paymentElement.mount('#payment-element');

const form = document.getElementById('payment-form');
form.addEventListener('submit', async (event) => {
event.preventDefault();

const {error} = await stripe.confirmPayment({
//`Elements` instance that was used to create the Payment Element
elements,
confirmParams: {
return_url: 'https://example.com/order/123/complete',
},
});

if (error) {
// This point will only be reached if there is an immediate error when
// confirming the payment. Show error to your customer (for example, payment
// details incomplete)
const messageContainer = document.querySelector('#error-message');
messageContainer.textContent = error.message;
} else {
// Your customer will be redirected to your `return_url`. For some payment
// methods like iDEAL, your customer will be redirected to an intermediate
// site first to authorize the payment, then redirected to the `return_url`.
}
});