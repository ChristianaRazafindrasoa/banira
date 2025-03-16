mapboxgl.accessToken = 'pk.eyJ1IjoiY2hyaXN0aWFuYTg2IiwiYSI6ImNtN214Y2swZTBuejQybnB2bDB1dml3cHMifQ.A3-fwlw292PiGiI9QnJ1VQ';
const map = new mapboxgl.Map({
    container: 'map', // ID of the div where the map will be rendered
    style: 'mapbox://styles/mapbox/streets-v12', // Map style
    center: [-18.91368,47.53613], // Starting position [lng, lat] 
    zoom: 5 // Zoom level
});
map.addControl(new mapboxgl.NavigationControl());

const coordinates = [
    {lat:47.53613, long:-18.91368, name:"Madagascar"},
    {lat:-81.5158, long:27.6648, name:"Florida"}
]

let coordinateIndex = 0;
let marker = null;

const button = document.getElementById('next');
button.addEventListener('click', nextButtonClicked);

function nextButtonClicked() {
    let coord = coordinates[coordinateIndex];
    const popup = new mapboxgl.Popup({ offset: 25 }).setText(coord.name);
    marker = new mapboxgl.Marker()
        .setLngLat([coord.lat, coord.long])
        .setPopup(popup)
        .addTo(map);

    map.flyTo({
        center: [coord.lat, coord.long],
        essential: true // this animation is considered essential with respect to prefers-reduced-motion
    });
    popup.addTo(map);
    coordinateIndex = (coordinateIndex + 1) % coordinates.length;
}
nextButtonClicked();

function drawLine(start, end) {
    const route = {
        'type': 'geojson',
        'data': {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [start.lat, start.lng], // Start point [lng, lat]
                    [end.lat, end.lng]  // End point [lng, lat]
                ]
            }
        }
    };
    map.addSource('route', route);

    map.addLayer({
        'id': 'route',
        'type': 'line',
        'source': 'route',
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': '#ff0000',
            'line-width': 4
        }
    });
}

const response = fetch("http://localhost:8080/api/network?origin=mad")
    .then(response => {
        if (!response.ok) {
            throw new Error();
        }
        return response.json();
    })
    .then(response => {
        console.log(response);
        console.log(response.edges);
        drawLine(response.edges[0].start, response.edges[0].end);
    })
