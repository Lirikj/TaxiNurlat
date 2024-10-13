const But1 = document.querySelector("button");
function initMap() {
    var map = new DG.Map('map', {
        center: [54.4354, 50.8085],
        zoom: 14
    });
}
function callTaxi() {
    But1.textContent = "уже выезжаем...";
    var destinationFrom = document.getElementById("destination_to").value;
    var destinationTo = document.getElementById("destination_from").value;
    alert("Вызываем такси от " + destinationTo + " до " + destinationFrom);
}
function getCurrentLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;
        });
    } else {
        alert("Геолокация не поддерживается вашим браузером");
    }
}
