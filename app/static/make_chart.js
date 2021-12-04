var t = document.getElementById("selector")
var b = t.getElementsByTagName("button")
console.log(b.length)
for (i = 0; i < b.length; i++){
    b[i].addEventListener("click", function () { makeChart(this.value); })
}
    

function show(data) {
    var graphs = data | safe;
    var layout = {
        autosize: false,
        width: 500,
        height: 500,
        margin: {
          l: 50,
          r: 50,
          b: 100,
          t: 100,
          pad: 4
        },
        paper_bgcolor: '#7f7f7f',
        plot_bgcolor: '#c7c7c7'
      };

    Plotly.plot('chart',graphs,layout);
}



function makeChart(value) {
    const url =`/main/chart?chart_name=${value}`
    fetch(url)
        .then((resp) => resp.json())
        .then(function (data) {
            var fig = JSON.parse(data)
            Plotly.newPlot('chart', fig.data, fig.layout)
        })
    .catch(function(error) {
        console.log(error);
    });
}