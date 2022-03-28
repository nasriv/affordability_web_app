// ensure library load
console.log(d3)
console.log(topojson)

// define data path urls
let stateURL = "https://cdn.jsdelivr.net/npm/us-atlas@3/states-albers-10m.json"
let countyURL = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-albers-10m.json"

let dataStateURL = "/static/map/data/statePopData.csv"

let stateGeoData
let countyGeoData
let statePopData
let countyPopData

let canvasState = d3.select('#canvas-state');
let canvasCounty = d3.select('#canvas-county');

// draw maps
let drawMap = () => {

    canvasState.selectAll('path')
        .data(stateGeoData)
        .enter()
        .append('path')
        .attr('d', d3.geoPath())
        .attr('stroke', 'black')
        .attr('stroke-linejoin', 'round')
        .attr('fill', (stateDataItem) => {
            let id = stateDataItem['id']
            let state = statePopData.find((item) => {
                return item['STATE'] === id
            })

            let pop = state['POPESTIMATE2021']
            if(pop <= 1000000){
                return 'tomato'
            }else if(pop <= 5000000){
                return 'orange'
            }else if(pop <= 15000000){
                return 'lightgreen'
            }else{
                return 'limegreen'
            }
        })

// map out county data
    canvasCounty.selectAll('path')
        .data(countyGeoData)
        .enter()
        .append('path')
        .attr('d', d3.geoPath())
}

// convert data to js objects
d3.json(stateURL).then(
    (data, error) => {
        if (error) {
            console.log(error);
        } else {
            stateGeoData = topojson.feature(data, data.objects.states).features
            console.log(stateGeoData);

            d3.json(countyURL).then(
                (data, error) => {
                    if (error) {
                        console.log(error);
                    } else {
                        countyGeoData = topojson.feature(data, data.objects.counties).features
                        console.log(countyGeoData);

                        d3.csv(dataStateURL).then(
                            (data, error) => {
                                if (error) {
                                    console.log(error);
                                } else {
                                    statePopData = data
                                    console.log(statePopData);

                                    // call function to draw map
                                    drawMap()
                                }
                            }
                        )

                    }
                }
            )
        }
    });