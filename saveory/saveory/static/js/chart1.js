new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels : [{% for item in labels %}
                  "{{item}}",
              {% endfor %}],
    datasets: [{ 
        data : [{% for item in values1 %}
                      {{item}},
                    {% endfor %}],
        label: "current month",
        borderColor: "#3e95cd",
        fill: false
      }, { 
        data : [{% for item in values2 %}
                      {{item}},
                    {% endfor %}],
        label: "last month",
        borderColor: "#8e5ea2",
        fill: false
      }
    ]
  },
  options: {
    title: {
      display: true,
      text: 'Gazoline spend month over month'
    }
  }
});