function add_title(svg, width){
  svg.append('text')
  .attr('x', width/2 + 100)
  .attr('y', 100)
  .attr('text-anchor', 'middle')
  .style('font-family', 'Helvetica')
  .style('font-size', 20)
  .text('7-Day Moving Daily Average');
}

function rolling_graph(name, data){
  var svg = d3.select(name),
          margin = 200,
          width = svg.attr("width") - margin,
          height = svg.attr("height") - margin 
  var xScale = d3.scaleTime().domain(d3.extent(data, function(d) { 
    return new Date(d[0]); 
  }))
  .range([0, width]), 
      yScale = d3.scaleLinear().domain([d3.min(data, function(d) { 
          return (0.9*d[1]); 
        }), d3.max(data, function(d) { 
          return (1.1*d[1]); 
        })]).range([height, 0]);  
      
  var g = svg.append("g")
      .attr("transform", "translate(" + 100 + "," + 100 + ")");

  add_title(svg, width)

  g.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(xScale).ticks(5));
  g.append("g")
  .call(d3.axisLeft(yScale).ticks(5));

  svg.append('g')
  .selectAll("dot")
  .data(data)
  .enter()
  .append("circle")
  .attr("cx", function (d) { return xScale(new Date(d[0])); } )
  .attr("cy", function (d) { return yScale(d[1]); } )
  .attr("r", 3)
  .attr("transform", "translate(" + 100 + "," + 100 + ")")
  .style("fill", "#CC0000"); 
  
  var line = d3.line()
  .x(function(d) { return xScale(new Date(d[0])); }) 
  .y(function(d) { return yScale(d[1]); }) 
  .curve(d3.curveMonotoneX)

  svg.append("path")
  .datum(data) 
  .attr("class", "line") 
  .attr("transform", "translate(" + 100 + "," + 100 + ")")
  .attr("d", line)
  .style("fill", "none")
  .style("stroke", "#CC0000")
  .style("stroke-width", "2")
              }
