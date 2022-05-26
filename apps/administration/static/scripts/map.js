const URL = 'http://127.0.0.1:6060';
let map_admin;

var greenIcon = L.icon({
    iconUrl: '/static/img/marker_icon_successful.png',
    iconSize:     [27, 40], // size of the icon
    popupAnchor:  [-3, -20] // point from which the popup should open relative to the iconAnchor
});

var redIcon = L.icon({
    iconUrl: '/static/img/marker_icon_error.png',
    iconSize:     [22, 40], // size of the icon
    popupAnchor:  [-3, -20] // point from which the popup should open relative to the iconAnchor
});

function map_init_basic (map) {
    map_admin = map;
}

fetch(`${URL}/administration/map_building/`).then(res => res.json()).then(res => {
    console.log("fetch")
    for (let i = 0; i < res.length; i++) {
        console.log("loop");
        if(res[i].is_inspection_successful){
            myMarker = L.marker([res[i].lat, res[i].lng],{icon: greenIcon}).addTo(map_admin);
            myMarker.bindPopup("Nombre: " + res[i].site_name + "<br>"+ "Tipo edificio: " + res[i].site_type + "<br> Inspeccion: Aprobada");
        }else if(res[i].is_inspection_successful == false){
            L.circle([res[i].lat, res[i].lng], {radius: 20, color: '#b20600'}).addTo(map_admin);
            myMarker = L.marker([res[i].lat, res[i].lng],{icon: redIcon}).addTo(map_admin);
            myMarker.bindPopup("Nombre: " + res[i].site_name + "<br>"+ "Tipo edificio: " + res[i].site_type + "<br> Inspeccion: No aprobada");
        }else{
            myMarker = L.marker([res[i].lat, res[i].lng]).addTo(map_admin);
            myMarker.bindPopup("Nombre: " + res[i].site_name + "<br>"+ "Tipo edificio: " + res[i].site_type + "<br> Inspeccion: Sin inspeccionar");
        }
    } 
}).catch(err => err);