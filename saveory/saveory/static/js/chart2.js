new Chart(document.getElementById("doughnut-chart"), {
    type: 'doughnut',
    data: {
    labels : [{% for item in labels %}
                  "{{item}}",
              {% endfor %}],      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data : [{% for item in values %}
                      {{item}},
                    {% endfor %}]        }
      ]
    },
    options: {
    
      }
    }
});