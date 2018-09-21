    var series = new Array();
    var interal_time ;
    $.ajax({
        url: "/timeinternalresponse/",
        dataType: "json",
        async:false,
        success: function (data) {
            interal_time = data.t * 1000;
            console.log(interal_time);
        }
    });
    Highcharts.setOptions({
    global: {
        useUTC: false
    }
    });
    Highcharts.chart('chart_container', {
    chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {
                for(var i=0;i<5;i++){
                    series[i] = this.series[i];
                }

                setInterval(function () {
                    var x; // current time
                    var y= new Array();
                    $.ajax({
                        url: "/qosresponse/",
                        dataType: "json",
                        async:false,
                        success: function (data) {
                            x = (new Date()).getTime(); // current time
                            for(var i=0;i<5;i++){
                                y[i] = data.a[i];
                                series[i].addPoint([x, y[i]], true, true);
                            }
                        }
                     })
                },interal_time);
            }
        }
    },
    title: {
        text: 'WEB服务QOS采集图像'
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: '响应时间'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x+"ms") + '<br/>' +
                Highcharts.numberFormat(this.y, 2);
        }
    },
    legend: {
        enabled:true
    },
    exporting: {
        enabled: false
    },
    series: [{
      name: 'WS1',
      data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 1000,
                    y: 0
                });
            }
            return data;
        }())
    },{
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 1000,
                    y: 0
                });
            }
            return data;
        }()),
        name: 'WS2'
    },{
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 1000,
                    y: 0
                });
            }
            return data;
        }()),
        name: 'WS3'
    },{
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 1000,
                    y: 0
                });
            }
            return data;
        }()),
        name: 'WS4'
    },{
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 1000,
                    y: 0
                });
            }
            return data;
        }()),
        name: 'WS5'
    }]
    });




