new Chart(document.getElementById("bar-chart-grouped"), {
    type: 'bar',
    data: {
      labels: ["January","February","March","April","May","June","July","August"],
      datasets: [
        {
          label: "income",
          backgroundColor: "#00FF00",
          data: [5000,6000,8000,2478, 7000, 6000, 4500,10000]
        }, {
          label: "outcome",
          backgroundColor: "#FF0000 ",
          data: [6000,5473,6750,7340, 7000, 5000, 4500, 9000]
        }
      ]
    },
    options: {
      title: {
        display: true,
        text: 'Months comparasion'
      }
    }
});
