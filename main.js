

console.log("mister my love");
mapboxgl.accessToken = 'pk.eyJ1IjoiY2hyaXN0aWFuYTg2IiwiYSI6ImNtN214Y2swZTBuejQybnB2bDB1dml3cHMifQ.A3-fwlw292PiGiI9QnJ1VQ';
const map = new mapboxgl.Map({
    container: 'map', // ID of the div where the map will be rendered
    style: 'mapbox://styles/mapbox/streets-v12', // Map style
    center: [47.53613,-18.91368], // Starting position [lng, lat] (Los Angeles)
    zoom: 5 // Zoom level
});
map.addControl(new mapboxgl.NavigationControl());
