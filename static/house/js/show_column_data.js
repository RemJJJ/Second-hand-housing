function column_chart(data) {
    var salaru_line = echarts.init(document.getElementById('scolumn_line'));
    
    // 设置容器高度
    var container = document.getElementById('scolumn_line');
    if (container) {
        container.style.height = "300px";
        container.style.width = "100%";
    }
    
    window.addEventListener('resize', function () {
        salaru_line.resize();
    });
    var XData = data['name_list_x']; // X轴的数据
    var YData = data['num_list_y'];  // Y轴的数据

    var dataMin = parseInt(Math.min.apply(null, YData) / 2);

    var option = {
        backgroundColor: "#fff",
        grid: {
            height: '200px',
            width: '320px',
            left: '50px',
            right: '20px',
            bottom: '60px'  // 增加底部空间给X轴文字
        },
        xAxis: {
            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
            splitArea: {
                show: false
            },
            data: XData,
            axisLabel: {
                formatter: function (value) {
                    // 简化文字处理，只显示前4个字符
                    if (value.length > 4) {
                        return value.substring(0, 4) + '...';
                    }
                    return value;
                },
                interval: 0,
                fontSize: 10,
                fontWeight: 100,
                textStyle: {
                    color: '#555',
                },
                rotate: 45  // 旋转文字避免重叠
            },
            axisLine: {
                show: {
                    color: '#4d4d4d'
                }
            }
        },
        yAxis: {
            name: '房源数量',
            nameLocation: 'center',
            nameGap: 35,

            axisTick: {
                show: false
            },
            splitLine: {
                show: false
            },
            splitArea: {
                show: false
            },
            min: dataMin,
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
        "tooltip": {
            "trigger": "item",
            "textStyle": {
                "fontSize": 12
            },
            "formatter": function(params) {
                return params.name + '<br/>房源数量: ' + params.value + '套';
            }
        },
        series: [{
            type: "bar",
            barWidth: '40%',  // 设置柱子宽度为40%
            itemStyle: {
                normal: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [{
                            offset: 0,
                            color: '#00d386' // 0% 处的颜色
                        }, {
                            offset: 1,
                            color: '#0076fc' // 100% 处的颜色
                        }],
                        globalCoord: false // 缺省为 false
                    },
                    barBorderRadius: 8,  // 减小圆角
                }
            },
            data: YData,
            label: {
                show: false  // 不显示柱子上的数量标签
            }
        }]
    };
    salaru_line.setOption(option, true);
}