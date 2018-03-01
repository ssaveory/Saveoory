new Chart(document.getElementById("bar-chart-grouped"), {
    type: 'bar',
    data: {
      labels: ["January","February","March","April","May","June","July","August"],
      datasets: [
        {
          label: "income",
          backgroundColor: "#00FF00",
          data : [{% for item in values1 %}
                      {{item}},
                    {% endfor %}]        }, {
          label: "outcome",
          backgroundColor: "#FF0000 ",
          data : [{% for item in values2 %}
                      {{item}},
                    {% endfor %}]        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Months comparasion'
      }
    }
});
