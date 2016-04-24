"use strict";
var formatDate = d3.time.format("%Y-%m-%d %I:%M %p");

var dateString = d3.time.format("%A, %b. %d");

var timeString = d3.time.format("%I:%M %p");

var transformData = function(d) {
    d.date = formatDate.parse(d.date);
    d.temperature = Math.round( +d.temperature *  10 ) / 10;
    d.humidity = Math.round( +d.humidity * 10 ) / 10;
    return d;
};

var drawTemp = function(data) {

  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 720 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;



  var x = d3.time.scale()
      .range([0, width]);

  var y = d3.scale.linear()
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

  var line = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.temperature); });

  var svg = d3.select("#temp-graph").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    console.log(d3.extent(data, function(d) { return d.date; }));

    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain(d3.extent(data, function(d) { return d.temperature; }));

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Temperature (F)");

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);

};

$(function(){
  var sortDate = function(a, b) {
    return b.date - a.date;
  };


  _.template.formatdate = function (stamp) {
    return dateString(stamp);
  };

  _.template.formattime = function(stamp) {
    return timeString(stamp);
  }

  var data;
  var readingTemp = _.template(
    $("#readingTemplate").html()
  );

  d3.csv('./data/readings.csv', transformData, function(error, data){
    if (error) throw error;
    console.log(data[65]);
    var lastReading = readingTemp(data[data.length]);
    $("#reading").html(lastReading);
    drawTemp(data);
  });

  // d3.csv('./data/readings.csv', function(d){
  //   return {
  //     timestamp : new Date(d.date),
  //     temperature : +d.temperature,
  //     humidity : +d.humidity,
  //   };
  // }, function(error, rows){
  //   return rows;
  // });

console.log(data);
});
