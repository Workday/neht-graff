


function toggle_tip(d) {
    /**
     * If the tooltip is visible, hide the tooltip.
     * If the tooltip is hidden, display the tooltip near the specified node
     * and display the node's properties
     * @param d dictionary representing data bound to a specific node
     */
    let node = d3.select('#node' + d.id);
    if (node.attr('tooltip') === 'hidden') {
        node.attr('tooltip', 'visible');
        let x = d3.event.pageX;
        let y = d3.event.pageY;
        d3.select('.tooltipContainer')
            .style('left', x + 10 + 'px')
            .style('top', y + 10 + 'px')
            .style('display', 'grid');
        d3.select('.tooltip')
            .html(node_tooltip(d));
    } else {
        node.attr('tooltip', 'hidden');
        d3.select('.tooltipContainer')
            .style('display', 'none');
    }
}

function show_query_bar() {
    /**
     * Display the tooltip query bar
     */
    d3.select('.tooltipQueryContainer')
        .style('display', 'grid');
}

function hide_query_bar() {
    /**
     * Hide the tooltip query bar
     */
    d3.select('.tooltipQueryContainer')
        .style('display', 'none');
}

function toggle_query_bar() {
    /**
     * If the tooltip query bar is currently displayed, hide the query bar.
     * Otherwise, show the query bar
     */
    let query_bar_display = d3.select('.tooltipQueryContainer')
        .style('display');
    if(query_bar_display === 'none') {
        show_query_bar();
    } else {
        hide_query_bar();
    }
}

function get_tooltip_query() {
    /**
     * Get the current text content of the query bar
     */
    return d3.select('.tooltipQueryBar')
        .property('value');
}