mapboxgl.accessToken =
  "pk.eyJ1Ijoic2plcmVteSIsImEiOiJjazI2MXA2MWcweXZyM2NxbWVyOTBtMWk1In0.Q7DN3I1YvMyCmCUPlrA30A";

    
//   const aa = {
//     "type": "FeatureCollection",
//     "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
//     "features": [
//     { "type": "Feature", "properties": { "id": "ak16994521", "mag": 2.3, "time": 1507425650893, "felt": null, "tsunami": 1 }, "geometry": { "type": "Point", "coordinates": [ -73.968565, 40.779897, 0.0 ] } },
//     ]};

var map = new mapboxgl.Map({
  container: "map", // container id
  style: "mapbox://styles/mapbox/dark-v10", // style URL
  center: [-73.968565, 40.779897], // starting position [lng, lat]
  zoom: 12, // starting zoom
});

map.on("load", function () {
  // Add a new source from our GeoJSON data and
  // set the 'cluster' option to true. GL-JS will
  // add the point_count property to your source data.
  map.addSource("randomtest", {
    type: "geojson",
    // Point to GeoJSON data. This example visualizes all M1.0+ randomtest
    // from 12/22/15 to 1/21/16 as logged by USGS' Earthquake hazards program.
    data: myData,
    cluster: true,
    clusterMaxZoom: 14, // Max zoom to cluster points on
    clusterRadius: 50, // Radius of each cluster when clustering points (defaults to 50)
  });
  map.on('error', e => {
    // Hide those annoying non-error errors
    if (e && e.error !== 'Error: Not Found')
        console.error(e);
});

  map.addLayer({
    id: "clusters",
    type: "circle",
    source: "randomtest",
    filter: ["has", "point_count"],
    paint: {
      // Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
      // with three steps to implement three types of circles:
      //   * Blue, 20px circles when point count is less than 100
      //   * Yellow, 30px circles when point count is between 100 and 750
      //   * Pink, 40px circles when point count is greater than or equal to 750
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
    source: "randomtest",
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
    source: "randomtest",
    filter: ["!", ["has", "point_count"]],
    paint: {
      "circle-color": "#11b4da",
      "circle-radius": 4,
      "circle-stroke-width": 1,
      "circle-stroke-color": "#fff",
    },
  });
});
