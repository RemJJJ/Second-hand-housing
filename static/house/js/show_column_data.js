function column_chart(data) {
    var salaru_line = echarts.init(document.getElementById('scolumn_line'));
    
    // 移除JS设置容器高度和宽度，改为用CSS控制
    // window.addEventListener('resize', function () {
    //     salaru_line.resize();
    // });
    // 防止重复绑定resize
    if (!window._scolumn_line_resize_bound) {
        window.addEventListener('resize', function () {
            salaru_line.resize();
        });
        window._scolumn_line_resize_bound = true;
    }
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
            barWidth: '45%',
            minBarHeight: 8, // 设置最小柱高，保证小数据也能看到
            itemStyle: {
                normal: {
                    color: {
                        type: 'linear',
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            { offset: 0, color: '#6dd5ed' }, // 渐变色更现代
                            { offset: 1, color: '#2193b0' }
                        ],
                        globalCoord: false
                    },
                    barBorderRadius: [8, 8, 0, 0],
                    shadowColor: 'rgba(33,147,176,0.18)',
                    shadowBlur: 8
                }
            },
            data: YData,
            label: {
                show: true,
                position: 'top',
                color: '#2193b0',
                fontWeight: 'bold',
                fontSize: 13,
                rotate: 45, // 让数字斜着显示
                formatter: function(val){
                    return val.value > 0 ? val.value : '';
                }
            },
            emphasis: {
                itemStyle: {
                    color: '#0076fc',
                    shadowColor: 'rgba(0,118,252,0.25)',
                    shadowBlur: 12
                }
            }
        }]
    };
    salaru_line.setOption(option, true);
}