const URL = 'http://127.0.0.1:6060';

var greenIcon = L.icon({
    iconUrl: '/static/img/marker_icon_successful.png',
    iconSize:     [22, 40], // size of the icon
    popupAnchor:  [-3, -20] // point from which the popup should open relative to the iconAnchor
});

var redIcon = L.icon({
    iconUrl: '/static/img/marker_icon_error.png',
    iconSize:     [22, 40], // size of the icon
    popupAnchor:  [-3, -20] // point from which the popup should open relative to the iconAnchor
});

function map_init_basic (map) {
    myMarker = L.marker([6.25184, -75.56359], {icon: redIcon}).addTo(map);
    myMarker.bindPopup("Tipo edificio: A1 <br> Inspeccion: Fallida");
    L.circle([6.25184, -75.56359], {radius: 20, color: '#b20600'}).addTo(map);
    L.marker([6.25184, -75.56],{icon: greenIcon}).addTo(map);
}

fetch(`${URL}/administration/map_building/`).then(res => res.json()).then(res => {
    console.log(res[0].lat + ", " + res[0].lng);
}).catch(err => err);