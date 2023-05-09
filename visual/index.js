// Initialize chart
const chartDom = document.getElementById('map');
const chart = echarts.init(chartDom);
let option;
chart.showLoading();

// Resize chart when window size changes
window.addEventListener('resize', () => {
    chart.resize();
}, true);

// Fetch USA layout and case data
Promise.all([
    fetch('USA.json').then(resp => resp.json()),
    fetch('all.json').then(resp => resp.json())
]).then(data => {
    const usaJson = data[0];

    const casesJson = data[1];
    casesJson.sort((first, second) => {
        return new Date(second.date) - new Date(first.date);
    });

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
                    '#e0f3f8',
                    '#abd9e9',
                    '#74add1',
                    '#4575b4',
                    '#313695',
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

    chart.on('click', (params) => {
        if (params.name) {
            const state = params.name;

            const caseHeading = document.getElementById('case-heading');
            caseHeading.innerText = 'Cases in ' + state;

            const caseList = document.getElementById('case-list');
            caseList.replaceChildren(...casesJson.filter((courtCase) => courtCase.state === state).map((courtCase) => {
                const listItem = document.createElement('li');

                const header = document.createElement('h3');
                header.innerText = courtCase.title;

                const date = document.createElement('span');
                date.innerText = new Date(courtCase.date).toLocaleDateString('en-us', { day: '2-digit', year: 'numeric', month: 'long'});

                const brief = document.createElement('p');
                brief.innerText = courtCase['desc'];

                const link = document.createElement('a');
                link.text = 'Read More';
                link.href = courtCase.url;

                listItem.append(header, date, brief, link);

                return listItem;
            }));
        }
    });
});

option && chart.setOption(option);
