mapboxgl.accessToken =
  "pk.eyJ1Ijoic2plcmVteSIsImEiOiJjazI2MXA2MWcweXZyM2NxbWVyOTBtMWk1In0.Q7DN3I1YvMyCmCUPlrA30A";


var map = new mapboxgl.Map({
  container: "map", // container id
  style: "mapbox://styles/mapbox/dark-v10", 
  center: [-73.968565, 40.779897], 
  zoom: 10, 
});

map.on("load", function () {
  // Add a new source from our GeoJSON data and
  // set the 'cluster' option to true. GL-JS will
  // add the point_count property to your source data.
  map.addSource("pickups", {
    type: "geojson",
    data: pickups_data,
    cluster: true,
    clusterMaxZoom: 14, // Max zoom to cluster points on
    clusterRadius: 50, // Radius of each cluster when clustering points (defaults to 50)
  });
  map.on('error', e => {
    if (e && e.error !== 'Error: Not Found')
        console.error(e);
});

  map.addLayer({
    id: "clusters",
    type: "circle",
    source: "pickups",
    filter: ["has", "point_count"],
    paint: {
      "circle-color": [
        "step",
        ["get", "point_count"],
        "#51bbd6",
        100,
        "#f1f075",
        750,
        "#f28cb1",
      ],
      "circle-radius": ["step", ["get", "point_count"], 20, 100, 30, 750, 40],
    },
  });

  map.addLayer({
    id: "cluster-count",
    type: "symbol",
    source: "pickups",
    filter: ["has", "point_count"],
    layout: {
      "text-field": "{point_count_abbreviated}",
      "text-font": ["DIN Offc Pro Medium", "Arial Unicode MS Bold"],
      "text-size": 12,
    },
  });

  map.addLayer({
    id: "unclustered-point",
    type: "circle",
    source: "pickups",
    filter: ["!", ["has", "point_count"]],
    paint: {
      "circle-color": "#11b4da",
      "circle-radius": 4,
      "circle-stroke-width": 1,
      "circle-stroke-color": "#fff",
    },
  });
});
