var ctx = document.getElementById("myChart").getContext('2d');
            ctx.canvas.width = 300;
            ctx.canvas.height = 300;
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ["Gazoline", "Supermarket", "restaurant", "hangouts", "drugs", "water bill",
                     "electric bill", "rent", " clothes", "vacation", "gifts", "health", "sports", "pleasure", "others"],
                    datasets: [{
                        label: '# of Votes',
                        data : [{% for item in values %}
                      {{item}},
                    {% endfor %}]                       
                     backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)',
                            'rgba(76, 76, 178, 0.8)',

                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,

                    scales: {
                        xAxes: [{
                            ticks: {
                                beginAtZero:true,
                                fontSize: 20,
                            }
                        }]
                        
                    }

                }
            });