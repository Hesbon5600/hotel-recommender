document.getElementById("createHotel").addEventListener("submit", createHotel);
// let Message = document.getElementById("Message");
// This function Authenticates the user then logs in the user
function createHotel(e) {
  e.preventDefault();
  let csrfToken = getCookie("csrftoken");

  let name = document.getElementById("name").value;
  let location = document.getElementById("location").value;
  let description = document.getElementById("description").value;
  let price = document.getElementById("price").value;
  let street_address = document.getElementById("streetAddress").value;
  let extended_address = document.getElementById("extendedAddress").value;
  let postal_code = document.getElementById("postalCode").value;
  let region = document.getElementById("region").value;
  let rating = document.getElementById("rating").value;
  let reviews = document.getElementById("reviews").value;
//   let hotel_image = document.getElementById("hotel-image").value;
  console.log(name, location, description);
  fetch("/apps/v1/hotels/hotel", {
    method: "POST",
    // mode: "cors",
    headers: {
      "Content-type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      name: name,
      location: location,
      description: description,
      price: price,
      street_address: street_address,
      extended_address: extended_address,
      postal_code: postal_code,
      region: region,
      rating: rating,
      reviews: reviews,
    //   hotel_image: hotel_image,
    }),
  }).then((res) => {
    // res.json()
    console.log(res.json())
  });
  // .then((data) => {
  //     if(data.message === "Successfully logged in"){
  //         getUserInfo(username);
  //         localStorage.setItem("token", data.token);
  //     }
  //     else{
  //         Message.innerHTML = data.message;
  //     }
  // })
}
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
