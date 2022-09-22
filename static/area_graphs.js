function area_graph(data, color, labels, title){

  const strokeWidth = 1.5;
  const margin = { top: 0, bottom: 20, left: 40, right: 20 };
  const chart = svg.append("g").attr("transform", `translate(${margin.left},0)`);

  const width = +svg.attr("width") - margin.left - margin.right - strokeWidth * 2;
  const height = +svg.attr("height") - margin.top - margin.bottom;
  const grp = chart
    .append("g")
    .attr("transform", `translate(-${margin.left - strokeWidth},-${margin.top})`);

  // Create stack
  const stack = d3.stack().keys(labels); // Needs to be variable, can set from Python
  const stackedValues = stack(data);
  const stackedData = [];
  // Copy the stack offsets back into the data.
  stackedValues.forEach((layer, index) => {
    const currentStack = [];
    layer.forEach((d, i) => {
      currentStack.push({
        values: d,
        date: new Date(data[i].date)
      });
    });
    stackedData.push(currentStack);
  });

  svg.append('text')
  .attr('x', width/2 + margin.left)
  .attr('y', margin.bottom)
  .attr('text-anchor', 'middle')
  .style('font-family', 'Helvetica')
  .style('font-size', 20)
  .text(title); //Need to be variable

  // Create scales
  const yScale = d3
    .scaleLinear()
    .range([height, 0])
    .domain([0, d3.max(stackedValues[stackedValues.length - 1], dp => 1.1*dp[1])]);
  const xScale = d3.scaleTime().domain(d3.extent(data, function(d) { 
          return new Date(d.date); 
        }))
        .range([0, width]);

  const area = d3
    .area()
    .x(dataPoint => xScale(new Date(dataPoint.date)))
    .y0(dataPoint => yScale(dataPoint.values[0]))
    .y1(dataPoint => yScale(dataPoint.values[1]));

  const series = grp
    .selectAll(".series")
    .data(stackedData)
    .enter()
    .append("g")
    .attr("class", "series");
  
  var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

  series
    .append("path")
    .attr("transform", `translate(${margin.left},0)`)
    .style("fill", (d, i) => color[i])
    .attr("stroke", "steelblue")
    .attr("stroke-linejoin", "round")
    .attr("stroke-linecap", "round")
    .attr("stroke-width", strokeWidth)
    .attr("d", d => area(d))
    .on('mouseover', function (d,i) {
      d3.select(this).transition()
           .duration('50')
           .attr('opacity', '.85');
      div.transition()
           .duration(50)
           .style("opacity", 1);
      div.html(labels[i])
           .style("left", (d3.event.pageX + 10) + "px")
           .style("top", (d3.event.pageY - 15) + "px");
    })
    .on('mouseout', function (d, i) {
      d3.select(this).transition()
           .duration('50')
           .attr('opacity', '1');
      div.transition()
           .duration('50')
           .style("opacity", 0);
    });

  // Add the X Axis
  chart
    .append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(xScale).ticks(5));

  // Add the Y Axis
  chart
    .append("g")
    .attr("transform", `translate(0, 0)`)
    .call(d3.axisLeft(yScale).ticks(5));
  }