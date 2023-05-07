import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";

const values = [
    {x: 0, y: 1},
    {x: 1, y: 2},
    {x: 2, y: 3},
    {x: 3, y: 4}
]

const width = 960, height = 500;

const x_scale = d3.scaleBand().range([0, width]).padding(0.1);
const y_scale = d3.scaleLinear().range([height, 0]);

const svg = d3.select("#map")
    .attr("width", width)
    .attr("height", height);

// Scale the Domain
x_scale.domain(values.map((d) => d.x));
y_scale.domain([0, d3.max(values, (d) => d.y)]);

// add the rectangles for the bar chart
svg
    .selectAll("rect")
    .data(values)
    .join("rect")
    .attr("class", "bar")
    .attr("x", (d) => x_scale(d.x))
    .attr("y", (d) => y_scale(d.y))
    .attr("width", x_scale.bandwidth())
    .attr("height", (d) => height - y_scale(d.y));
