// Initialize chart
const chartDom = document.getElementById('map');
const chart = echarts.init(chartDom);
let option;
chart.showLoading();

// Fetch USA layout and case data
Promise.all([
    fetch('USA.json').then(resp => resp.json()),
    fetch('all.json').then(resp => resp.json())
]).then(data => {
    const usaJson = data[0];
    const casesJson = data[1];

    const states = casesJson.reduce((list, courtCase) => {
        if (!list.includes(courtCase.state))
            list.push(courtCase.state);
        return list;
    }, []);

    console.log(states);

    const totalCases = states.map((state) => {
        const count = casesJson.reduce((count, courtCase) => {
            if (courtCase.state === state)
                return count + 1;
            return count;
        } , 0);
        return { name: state, value: count };
    });

    console.log(totalCases);

    const minCases = 0;
    const maxCases = totalCases.reduce((oldMax, pair) => Math.max(oldMax, pair.value), 0);

    const projection = d3.geoAlbersUsa();
    chart.hideLoading();
    echarts.registerMap('USA', usaJson);
    option = {
        title: {
            text: 'LGBT Rights Legal Actions',
            subtext: 'Data from the ACLU and Lambda Legal',
            left: 'right'
        },
        tooltip: {
            trigger: 'item',
            showDelay: 0,
            transitionDuration: 0.2
        },
        visualMap: {
            left: 'right',
            min: minCases,
            max: maxCases,
            inRange: {
                color: [
                    '#313695',
                    '#4575b4',
                    '#74add1',
                    '#abd9e9',
                    '#e0f3f8',
                    '#ffffbf',
                    '#fee090',
                    '#fdae61',
                    '#f46d43',
                    '#d73027',
                    '#a50026'
                ]
            },
            text: ['High', 'Low']
        },
        toolbox: {
            show: true,
            //orient: 'vertical',
            left: 'left',
            top: 'top',
            feature: {
                dataView: { readOnly: false },
                restore: {},
                saveAsImage: {}
            }
        },
        series: [
            {
                name: 'Number of Cases',
                type: 'map',
                map: 'USA',
                projection: {
                    project: function (point) {
                        return projection(point);
                    },
                    unproject: function (point) {
                        return projection.invert(point);
                    }
                },
                emphasis: {
                    label: {
                        show: true
                    }
                },
                data: totalCases
            }
        ]
    };
    chart.setOption(option);
});

option && chart.setOption(option);
