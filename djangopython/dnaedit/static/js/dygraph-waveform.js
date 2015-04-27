/*

dygraph-waveform.js
created April 13, 2015

functions built on the Dygraphs API to generate an LCM waveform graph

*/

/*
generateWaveform
function to create the list of points to be used to generate a visual graph
@param sequence - a DNA nucleotide sequence as a string
@return a list of x/y1/y2/y3/y4 pairs representing the A/T/G/C  waves
*/
function generateWaveform(sequence) {
            "use strict";
            var list = [],
            i;
            for (i = 0; i < sequence.length; i += 1) {
                if (sequence.charAt(i) === "A") {
                    list[list.length] = [i + 1 - 0.4, 0.2, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 - 0.2, 0.7, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.0, 1 + ((Math.random() - 0.375) / 4), Math.random() / 10, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.2, 0.7, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.4, 0.2, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                } else if (sequence.charAt(i) === "T") {
                    list[list.length] = [i + 1 - 0.4, Math.random() / 10, 0.2, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 - 0.2, Math.random() / 10, 0.7, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.0, Math.random() / 10, 1 + ((Math.random() - 0.375) / 4), Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.2, Math.random() / 10, 0.7, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.4, Math.random() / 10, 0.2, Math.random() / 10, Math.random() / 10];
                } else if (sequence.charAt(i) === "G") {
                    list[list.length] = [i + 1 - 0.4, Math.random() / 10, Math.random() / 10, 0.2, Math.random() / 10];
                    list[list.length] = [i + 1 - 0.2, Math.random() / 10, Math.random() / 10, 0.7, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.0, Math.random() / 10, Math.random() / 10, 1 + ((Math.random() - 0.375) / 4), Math.random() / 10];
                    list[list.length] = [i + 1 + 0.2, Math.random() / 10, Math.random() / 10, 0.7, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.4, Math.random() / 10, Math.random() / 10, 0.2, Math.random() / 10];
                } else if (sequence.charAt(i) === "C") {
                    list[list.length] = [i + 1 - 0.4, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.2];
                    list[list.length] = [i + 1 - 0.2, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.7];
                    list[list.length] = [i + 1 + 0.0, Math.random() / 10, Math.random() / 10, Math.random() / 10, 1 + ((Math.random() - 0.375) / 4)];
                    list[list.length] = [i + 1 + 0.2, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.7];
                    list[list.length] = [i + 1 + 0.4, Math.random() / 10, Math.random() / 10, Math.random() / 10, 0.2];
                } else {
                    list[list.length] = [i + 1 - 0.4, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 - 0.2, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.0, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.2, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                    list[list.length] = [i + 1 + 0.4, Math.random() / 10, Math.random() / 10, Math.random() / 10, Math.random() / 10];
                }
            }
            //for (i = 0; i < list.length; i += 1) {
            //    console.log(list[i]);
            //}
            return list;
        }
        /*
        drawGraph
        function to draw a waveform graph
        
        @param containingDiv - the HTML div element to place the graph in
        @param legendDiv - the HTML div element to place the graph's legend in
        @return - returns the dygraph object representing the graph itself
        */        
        function drawGraph(seq, containingDiv, legendDiv) {
            return new Dygraph(
                containingDiv,
                generateWaveform(seq),
                {
                  labels: ['x', 'A', 'T', 'G', 'C'],
                  series: {
                       A: {
                         color: 'blue',
                         strokeWidth: 1.25
                       },
                       T: {
                         color: 'red',
                         strokeWidth: 1.25
                       },
                       G: {
                         color: 'green',
                         strokeWidth: 1.25
                       },
                       C: {
                         color: 'magenta',
                         strokeWidth: 1.25
                       }
                    },
                  legend: 'always',
                  connectSeparatedPoints: true,
                  drawPoints: false,
                  width: seq.length > 1000 ? 30000 : 30*seq.length + 20,
                  height: 150,
                  labelsDiv: legendDiv, 
                  axes: {
                    y: {
                      drawAxis: true,   
                      drawGrid: false,
                      axisLabelFontSize: 0,
                      axisLineWidth: 1
                    },
                    x: {
                      //axisLabelFormatter: function(label) {
                      //   return (label + 1).toString()
                      //},
                      includeZero: true,
                      drawAxis: true,
                      drawGrid: false,
                      axisLabelFontSize: 14,
                      axisLineWidth: 1
                    }
                  }
                }
            ); 
        }
        /*
        drawGraphInPopup
        draws the waveform graph in a popup window
        
        @param seq - the DNA nucleotide sequence to generate the waveform for
        @return - the waveform dygraph object
        */
        function drawGraphInPopup(seq) {
            var graphWindow = window.open("about:blank", "_blank", "centerscreen, resizable, dialog, scrollbars, top=0, left=0, width=100, height=100");
            graphWindow.resizeTo(seq.length*30 + 120 > 2*screen.availWidth/3 ? 2*screen.availWidth/3 : seq.length*30 + 120, 300);
            graphWindow.document.write("<!DOCTYPE html><html><body><div id=\'graph\'></div><div id=\'labels\' style=\'position:fixed; padding-left: 5px; padding-right: 5px; padding-top: 5px; padding-bottom: 5px;\'></div></body></html>");
            graphWindow.document.getElementById("labels").style.outline = "thin solid #000000";
            return drawGraph(seq, graphWindow.document.getElementById('graph'), graphWindow.document.getElementById('labels')); 
        }
        
