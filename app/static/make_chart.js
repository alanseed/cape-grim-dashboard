var t = document.getElementById("selector")
var b = t.getElementsByTagName("button")

for (i = 0; i < b.length; i++){
    b[i].addEventListener("click", function () { makeChart(this.value); })
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