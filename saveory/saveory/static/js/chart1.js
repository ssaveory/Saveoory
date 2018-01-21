new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels: ["1","5","10","15","20","25","31"],
    datasets: [{ 
        data: [86,114,106,106,111,221,783],
        label: "current month",
        borderColor: "#3e95cd",
        fill: false
      }, { 
        data: [282,350,411,502,635,809,947],
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