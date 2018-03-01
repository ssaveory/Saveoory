new Chart(document.getElementById("bar-chart-horizontal"), {
    type: 'horizontalBar',
    data: {
      labels: ["you", "people like you"],
      datasets: [
        {
          label: "Amount",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data : [{% for item in values %}
                      {{item}},
                    {% endfor %}]        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: true,
        text: 'comparign you to people like you - category Electicity'
      }
    }
});
