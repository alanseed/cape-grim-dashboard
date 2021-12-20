var t = document.getElementById("selector")
var b = t.getElementsByTagName("button")

for (i = 0; i < b.length; i++){
    b[i].addEventListener("click", function () { makeChart(this.value); })
}
    
function makeChart(name) {
    const url =`chart?name=${name}`
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
