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

    // 动态获取户型数据
    var roomTypes = [];
    var seriesData = [];
    var colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e'];
    
    // 遍历数据，找出所有户型（除了date_li）
    for (var key in data) {
        if (key !== 'date_li' && Array.isArray(data[key])) {
            roomTypes.push(key);
        }
    }
    
    console.log('户型价格走势图 - 检测到的户型:', roomTypes);
    
    // 为每个户型创建系列数据
    roomTypes.forEach(function(roomType, index) {
        seriesData.push({
            name: roomType,
            type: 'line',
            smooth: true,
            data: data[roomType],
            itemStyle: {
                color: colors[index % colors.length]
            },
            lineStyle: {
                color: colors[index % colors.length],
                width: 2
            }
        });
    });

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
            data: roomTypes,
            top: 10,
            type: 'scroll'  // 如果户型太多，可以滚动
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
        series: seriesData
    };

    salaru_line.setOption(option, true);
}