function price_chart(data) {
    var price_line = echarts.init(document.getElementById('f_line'));
    
    // 设置容器高度
    var container = document.getElementById('f_line');
    if (container) {
        container.style.height = "300px";
        container.style.width = "100%";
    }
    
    window.addEventListener('resize', function () {
        price_line.resize();
    });
    
    var XData = data['name_list_x'];
    var YData = data['price_list_y'];

    var option = {
        backgroundColor: "#fff",
        grid: {
            height: '200px',
            width: '320px',
            left: '50px',
            right: '20px',
            bottom: '60px'
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: XData,
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
            axisLabel: {
                fontSize: 10,
                color: '#555',
                rotate: 45  // 旋转日期标签避免重叠
            },
            axisLine: {
                lineStyle: {
                    color: '#4d4d4d'
                }
            }
        },
        yAxis: {
            type: 'value',
            name: '平均价格/元',
            nameLocation: 'center',
            nameGap: 30,
            axisTick: {
                show: false
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: '#f0f0f0',
                    type: 'dashed'
                }
            },
            axisLabel: {
                textStyle: {
                    color: '#9faeb5',
                    fontSize: 12,
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#4d4d4d'
                }
            }
        },
        tooltip: {
            trigger: 'axis',
            formatter: function(params) {
                return params[0].name + '<br/>' + 
                       params[0].seriesName + ': ' + params[0].value + '元/㎡';
            }
        },
        series: [{
            name: '价格走势',
            type: 'line',
            smooth: true,
            data: YData,
            itemStyle: {
                color: '#17a2b8'
            },
            lineStyle: {
                color: '#17a2b8',
                width: 3
            },
            areaStyle: {
                color: {
                    type: 'linear',
                    x: 0,
                    y: 0,
                    x2: 0,
                    y2: 1,
                    colorStops: [{
                        offset: 0,
                        color: 'rgba(23, 162, 184, 0.3)'
                    }, {
                        offset: 1,
                        color: 'rgba(23, 162, 184, 0.1)'
                    }]
                }
            },
            markPoint: {
                data: [
                    {type: 'max', name: '最高价'},
                    {type: 'min', name: '最低价'}
                ]
            },
            markLine: {
                data: [
                    {type: 'average', name: '平均值'}
                ]
            }
        }]
    };
    
    price_line.setOption(option, true);
} 