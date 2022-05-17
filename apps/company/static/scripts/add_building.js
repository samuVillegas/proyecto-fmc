let myMarker;
let map_l;
let arr_addr;

function map_init_basic (map) {
    map_l = map
    myMarker = L.marker([50.5, 30.5], {title: "Coordinates", alt: "Coordinates", draggable: true}).addTo(map).on('dragend', function() {
        var lat = myMarker.getLatLng().lat.toFixed(8);
        var lon = myMarker.getLatLng().lng.toFixed(8);
        document.getElementById('lat').value = lat;
        document.getElementById('lon').value = lon;
        console.log(lat,lon);
        myMarker.bindPopup("Lat " + lat + "<br />Lon " + lon).openPopup();
    });
    //myMarker = L.marker([50.5, 30.5]).addTo(map);S
}




function chooseAddr(lat1, lng1, id)
{
    myMarker.closePopup();
    map_l.setView([lat1, lng1],18);
    myMarker.setLatLng([lat1, lng1]);
    lat = lat1.toFixed(8);
    lon = lng1.toFixed(8);
    document.getElementById('lat').value = lat;
    document.getElementById('lon').value = lon;
    console.log(arr_addr[id].display_name);
    myMarker.bindPopup(arr_addr[id].display_name).openPopup();
}

function myFunction(arr)
{
    var out = "<br />";
    var i;
    arr_addr = arr;
    if(arr.length > 0)
    {
    for(i = 0; i < arr.length; i++)
    {
    out += "<div class='address' title='Show Location and Coordinates' onclick='chooseAddr(" + arr[i].lat + ", " + arr[i].lon + ", " + i + ");return false;'>" + arr[i].display_name + "</div>";
    }
    document.getElementById('results').innerHTML = out;
    }
    else
    {
    document.getElementById('results').innerHTML = "No se han encontrado lugares";
    }
}

function addr_search()
{
    var inp = document.getElementById("addr");
    var xmlhttp = new XMLHttpRequest();
    var url = "https://nominatim.openstreetmap.org/search?format=json&limit=3&q=" + inp.value;
    console.log(url);
    xmlhttp.onreadystatechange = function()
    {
    if (this.readyState == 4 && this.status == 200)
    {
    var myArr = JSON.parse(this.responseText);
    myFunction(myArr);
    }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}