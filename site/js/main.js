"use strict";
var formatDate = d3.time.format("%Y-%m-%d %I:%M %p");

var dateString = d3.time.format("%A, %b. %-d");

var timeString = d3.time.format("%-I:%M %p");

var transformData = function(d) {
    d.date = formatDate.parse(d.date);
    d.temperature = +d.temperature;
    d.humidity = +d.humidity;
    d.city_temperature = +d.city_temperature;
    d.city_humidity = +d.city_humidity;
    return d;
};

var drawChart = function(data, chartType) {
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 720 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;

  var x = d3.time.scale()
      .range([0, width]);

  var y = d3.scale.linear()
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom")
      .ticks(5)
      .tickFormat(d3.time.format("%-I:%M %p"));

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

  var localLine = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d[chartType]); });

  var wundergroundLine = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d['city_'+chartType]); });

  var svg = d3.select(".chart#" + chartType).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  x.domain(d3.extent(data, function(d) { return d.date; }));
  y.domain([
    d3.min(data, function(d){
      return d3.min([
        d[chartType],
        d['city_'+chartType]
      ]) - 10;
    }),
    d3.max(data, function(d) {
      return d3.max([
        d[chartType],
        d['city_'+chartType]
      ]) + 10;
    })
  ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

  svg.append("path")
      .datum(data)
      .attr("class", "line local")
      .attr("d", localLine);

  svg.append("path")
      .datum(data)
      .attr("class", "line wunderground")
      .attr("d", wundergroundLine);
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

  _.template.formatreading = function(reading) {
    return Math.round(reading * 10) / 10;
  }

  var data;
  var readingTemp = _.template(
    $("#readingTemplate").html()
  );

  d3.csv('./data/readings.csv', transformData, function(error, data){
    if (error) throw error;

    var lastReading = readingTemp(data[data.length - 1]);
    $("#reading").html(lastReading);

    drawChart(data, 'temperature');
    drawChart(data, 'humidity');
  });

});
