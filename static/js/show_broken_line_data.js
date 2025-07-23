function broken_line_chart(data) {

    var salaru_line = echarts.init(document.getElementById('broken_line'), 'infographic');
    
    // 设置容器高度
    var container = document.getElementById('broken_line');
    if (container) {
        container.style.height = "300px";
        container.style.width = "100%";
    }
    
    window.addEventListener('resize', function () {
        salaru_line.resize();
    });

    var Data1 = data['3室2厅'];
    var Data2 = data['2室2厅'];
    var Data3 = data['2室1厅'];
    var Data4 = data['1室1厅'];

    echartsDate = [];
    for (var i = 0; i < data['date_li'].length; i++) {
        d = data['date_li'][i]
        echartsDate.push(d);
    }

    var option = {
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                var result = params[0].name + '<br/>';
                params.forEach(function(param) {
                    result += param.marker + param.seriesName + ': ' + param.value + '元/㎡<br/>';
                });
                return result;
            }
        },
        legend: {
            data: ['3室2厅', '2室2厅', '2室1厅', '1室1厅'],
            top: 10
        },
        grid: {
            containLabel: true,
            left: '5%',
            right: '4%',
            bottom: '15%',
            top: '15%'
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: echartsDate,
            axisLabel: {
                rotate: 45,
                fontSize: 10
            }
        },
        yAxis: {
            type: 'value',
            name: '平均价格/元',
            nameLocation: 'center',
            nameGap: 30,
            axisLine:{show:true},
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#f0f0f0',
                    type: 'dashed'
                }
            }
        },
        series: [
            {
                name: '3室2厅',
                type: 'line',
                smooth: true,
                data: Data1,
                itemStyle: {
                    color: '#e74c3c'
                },
                lineStyle: {
                    color: '#e74c3c',
                    width: 2
                }
            },
            {
                name: '2室2厅',
                type: 'line',
                smooth: true,
                data: Data2,
                itemStyle: {
                    color: '#3498db'
                },
                lineStyle: {
                    color: '#3498db',
                    width: 2
                }
            },
            {
                name: '2室1厅',
                type: 'line',
                smooth: true,
                data: Data3,
                itemStyle: {
                    color: '#2ecc71'
                },
                lineStyle: {
                    color: '#2ecc71',
                    width: 2
                }
            },
            {
                name: '1室1厅',
                type: 'line',
                smooth: true,
                data: Data4,
                itemStyle: {
                    color: '#f39c12'
                },
                lineStyle: {
                    color: '#f39c12',
                    width: 2
                }
            }
        ]
    };

    salaru_line.setOption(option, true);
}