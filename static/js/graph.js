const NODE_GRAVITY = -900; // Positive values attract, negative values repel
const LINK_DISTANCE = 170;
const SVG_TAG = '#graphSvg';
const LINK_HIGHLIGHT_COLOR = '#ff0000';
const ENABLE_NODE_TEXT = true;   // display labels on nodes
const ENABLE_LINE_TEXT = false;  // display relationship labels on links (low performance)


if (json_data !== '') {
    const data = JSON.parse(json_data);

    let node_ids = [];
    let path_ids = [];

    for(let key in data.nodes) {
        node_ids.push(data.nodes[key].id)
    }
    for(let key in data.paths) {
        path_ids.push(data.paths[key].id)
    }

    let svg = d3.select(SVG_TAG);
    svg.attr('viewBox', [-500, -500, 1000, 1000]);

    // forces
    let link_force = d3.forceLink(data.paths)
        .distance(LINK_DISTANCE)
        .id(d => d.id);
    let charge_force = d3.forceManyBody()
        .strength(NODE_GRAVITY);
    let position_force_x = d3.forceX();
    let position_force_y = d3.forceY();

    let simulation = d3.forceSimulation()
        .nodes(data.nodes)
        .force('charge_force', charge_force)
        .force('x', position_force_x)
        .force('y', position_force_y)
        .force('links', link_force)
        .on('tick', tick_actions);

    // arrow svg which is displayed on the end of each link
    let arrow = svg.append('defs').append('marker')
        .attr('id', 'arrow')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 22)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 7)
        .attr('markerHeight', 7)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .style('fill', '#7b7b7b')
        .style('opacity', 1)
        .style('stroke', 'none');

    let circle_shadow = svg.select('defs')
        .append('filter')
        .attr('id', 'circle_shadow')
        .append('feDropShadow')
        .attr('dx', 0)
        .attr('dx', 0.3)
        .attr('stdDeviation', 0.2);


    let all_group = svg.append('g')
        .attr('class', 'all_group');

    let link_group = all_group.append('g')
        .attr('class', 'link_group')
        .selectAll('.link_line')
        .data(data.paths)
        .enter()
        .append('line')
        .attr('source', d => d.source.id)
        .attr('target', d => d.target.id)
        .attr('class', 'link_line')
        .attr('stroke-width', 2)
        .attr('marker-end', 'url(#arrow)')
        .style('stroke', d => link_color(d))
        .style('opacity', 1);

    let node_group = all_group.append('g')              // add a group element to all_group
        .attr('class', 'node_group')       // name the group "node_group"
        .selectAll('.node')
        .data(data.nodes)
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('pointer-events', 'all')
        .attr('id', function (d) {return 'node' + d.id})
        .attr('tooltip', 'hidden')
        .on('click', d => node_clicked(d))
        .on('dblclick', d => node_double_clicked(d));

    let node_circle_group = svg.selectAll('.node')
        .append('circle')
        .attr('class', 'node_circle')
        //.attr('filter', 'url(#circle_shadow)')
        .attr('opacity', 1)
        .attr('r', d => node_size(d))
        .attr('fill', d => node_color(d));

    if(ENABLE_NODE_TEXT) {
        let node_text_group = svg.selectAll('.node')
            .append('text')
            .attr('dx', '0')
            .attr('dy', '0')
            .attr('class', 'node_text')
            .style('pointer-events', 'none')
            .style('font-size', '.7em')
            .style('font-weight', 'lighter')
            .style('text-anchor', 'middle')
            .style('text-length', 17)
            .style('opacity', 1)
            .style('fill', d => node_text_color(d))
            .text(d => node_label(d));
    }

    let drag_handler = d3.drag()
        .on('start', drag_start)
        .on('drag', drag_drag)
        .on('end', drag_end);

    drag_handler(node_group);

    svg.call(d3.zoom()
        .scaleExtent([0, 9])
        .on('zoom', zoomed))
        .on('dblclick.zoom', null);

    svg.on('click', function() {deselect_node()});

    function zoomed() {
        /**
         * Perform zoom transformation on all elements under all_group
         */
        try {
            all_group.attr("transform", d3.event.transform);
        }
        catch(error) {
            if(error.name ==='TypeError') {
            }
            else {
                console.log(error)
            }
        }
    }

    function drag_start(d) {
        /**
         * Move the dragged node, then fix position in simulation
         */
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d3.event.x;
        d.fy = d3.event.y;
        d3.select(this).classed('fixed', d.fixed = true);
    }

    function drag_drag(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function drag_end(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function node_clicked(d) {
        /**
         *  Runs specified functions when a node is clicked
         */
        toggle_tip(d);
        toggle_highlight(d);
        assign_tooltip_buttons(d);
        d3.event.stopPropagation();  // Stops click event from propagating to the container SVG
    }

    function node_double_clicked(d) {
        //auto_pivot(d);
        //d3.event.stopPropagation();
    }

    function unpin_node(d) {
        /**
         * Removes fixed coordinates for a node, allowing it to continue to experience forces
         */
        d.fx = null;
        d.fy = null;
    }

    function set_legend() {
        // TODO generate legend based on link types
    }

    function set_statistics_text() {
        /**
         * Set the link and node counts displayed in the bottom left hand corner
         */
        d3.select('#statisticsContent')
            .html('Nodes: ' + data.nodes.length + '<br>'
        + 'Relationships: ' + data.paths.length)
    }

    set_statistics_text();

    let edgepath_group = all_group.append('g')
        .attr('class', 'edgepath_group')
        .selectAll('.edgepath')
        .data(data.paths)
        .enter()
        .append('path')
        .attr('class', 'edgepath')
        .attr('fill-opacity', 1)
        .attr('stroke-opacity', 1)
        .attr('id', function (d, i) {
            return 'edgepath' + i
        })
        .style("pointer-events", "none");

    if(ENABLE_LINE_TEXT) {
        let edgelabel_group = all_group.append('g')
            .attr('class', 'edgelabel_group')
            .selectAll(".edgelabel")
            .data(data.paths)
            .enter()
            .append('text')
            .style("pointer-events", "none")
            .attr('class', 'edgelabel')
            .attr('id', function (d, i) {
                return 'edgelabel' + i
            })
            .attr('font-size', 10)
            .attr('fill', '#808080');

        edgelabel_group.append('textPath')
            .attr('xlink:href', function (d, i) {
                return '#edgepath' + i
            })
            .style("text-anchor", "middle")
            .style("pointer-events", "none")
            .attr("startOffset", "50%")
            .text(function (d) {
                return d.type;
            });

        let edgelabel_move_group = d3.selectAll('.edgelabel');
    }
    let edgepath_move_group = d3.selectAll('.edgepath');
    let node_move_group = d3.selectAll('.node');
    let link_move_group = d3.selectAll('.link_line');

    function tick_actions() {
        /**
         * Specifies how each group of elements should transform on each simulation tick
         */
        node_move_group.attr('transform', function (d) {
            return 'translate(' + d.x + ',' + d.y + ')';
        });

        link_move_group
            .attr('x1', function (d) {
                return d.source.x;
            })
            .attr('y1', function (d) {
                return d.source.y;
            })
            .attr('x2', function (d) {
                return d.target.x;
            })
            .attr('y2', function (d) {
                return d.target.y;
            });

        edgepath_move_group.attr('d', function (d) {
            return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
        });

        if(ENABLE_LINE_TEXT) {
            edgelabel_move_group.attr('transform', function (d) {
                if (d.target.x < d.source.x) {
                    let bbox = this.getBBox();
                    let rx = bbox.x + bbox.width / 2;
                    let ry = bbox.y + bbox.height / 2;
                    return 'rotate(180 ' + rx + ' ' + ry + ')';
                } else {
                    return 'rotate(0)';
                }
            });
        }
    }

    function update_data(response_data) {
        /**
         * Add the new nodes and relationships to the existing dataset
         * @param response_data JSON containing nodes and relationships
         */
        for(let key in response_data.nodes) {
            let node = response_data.nodes[key];
            if(!(node_ids.includes(node.id))) {
                data.nodes.push(node);
                node_ids.push(node.id)
            }
        }
        for(let key in response_data.paths) {
            let path = response_data.paths[key];
            if(!(path_ids.includes(path.id))) {
                data.paths.push(path);
                path_ids.push(path.id);
            }
        }
    }

    function submit_query(query) {
        /**
         * Submit a new query from the tooltip query bar to Flask
         * If the response contains node and relationship data, add to current data and restart
         * the simulation.
         * If the response contains a Cypher syntax error, display the error as an alert
         */
        $.ajax({
            type: 'POST',
            contentType: 'application/json',
            url: '/submit_query',
            traditional: 'true',
            data: JSON.stringify(query),
            dataType: 'json',
            success: function (response_data) {
                if(response_data.hasOwnProperty('nodes')) {
                    update_data(response_data);
                    restart();
                } else {
                    alert(response_data);
                }
            }
        });
    }

    //set_legend();

    function restart() {
        /**
         * Restart the simulation to render an expanded data set
         */
        set_statistics_text();

        link_group = d3.select('.link_group')
            .selectAll('.link_line')
            .data(data.paths)
            .enter()
            .append('line')
            .attr('source', d => d.source)
            .attr('target', d => d.target)
            .attr('class', 'link_line')
            .attr('stroke-width', 2)
            .attr('marker-end', 'url(#arrow)')
            .style('stroke', d => link_color(d))
            .style('opacity', 1);

        node_group = d3.select('.node_group')
            .selectAll('.node')
            .data(data.nodes)
            .enter()
            .append('g')
            .attr('class', 'node')
            .attr('pointer-events', 'all')
            .attr('id', function (d) {
                return 'node' + d.id
            })
            .attr('tooltip', 'hidden')
            .on('click', d => node_clicked(d))
            .on('dblclick', d => node_double_clicked(d));
        node_group.append('circle')
            .attr('class', 'node_circle')
            .attr('opacity', 1)
            .attr('r', d => node_size(d))
            .attr('fill', d => node_color(d));

        if(ENABLE_NODE_TEXT) {
            node_group.append('text')
                .attr('dx', '0')
                .attr('dy', '0')
                .attr('class', 'node_text')
                .style('pointer-events', 'none')
                .style('font-size', '.7em')
                .style('font-weight', 'lighter')
                .style('text-anchor', 'middle')
                .style('text-length', 17)
                .style('opacity', 1)
                .style('fill', d => node_text_color(d))
                .text(d => node_label(d));
        }

        edgepath_group = all_group.select('.edgepath_group')
            .selectAll('.edgepath')
            .data(data.paths)
            .enter()
            .append('path')
            .attr('class', 'edgepath')
            .attr('fill-opacity', 1)
            .attr('stroke-opacity', 1)
            .attr('id', function (d, i) {
                return 'edgepath' + i
            })
            .style("pointer-events", "none");

        if(ENABLE_LINE_TEXT) {
            edgelabel_group = all_group.select('.edgelabel_group')
            .selectAll(".edgelabel")
            .data(data.paths)
            .enter()
            .append('text')
            .style("pointer-events", "none")
            .attr('class', 'edgelabel')
            .attr('id', function (d, i) {
                return 'edgelabel' + i
            })
            .attr('font-size', 10)
            .attr('fill', '#808080');

            edgelabel_group.append('textPath')
                .attr('xlink:href', function (d, i) {
                    return '#edgepath' + i
                })
                .style("text-anchor", "middle")
                .style("pointer-events", "none")
                .attr("startOffset", "50%")
                .text(function (d) {
                    return d.type;
                });
        }

        node_move_group = d3.selectAll('.node');
        link_move_group = d3.selectAll('.link_line');

        if(ENABLE_LINE_TEXT) {
            edgepath_move_group = d3.selectAll('.edgepath');
            edgelabel_move_group = d3.selectAll('.edgelabel');
        }

        drag_handler(node_group);

        simulation.nodes(data.nodes);
        link_force = d3.forceLink(data.paths)
            .distance(LINK_DISTANCE)
            .id(d => d.id);
        simulation.alpha(1).restart();

        try {
            svg.call(d3.zoom()
                .scaleExtent([0, 9])
                .on('zoom', all_group.attr("transform", d3.event.transform)))
                .on('dblclick.zoom', null);
        }
        catch(error) {
            if(error.name ==='TypeError') {
            }
            else {
                console.log(error)
            }
        }
    }
}