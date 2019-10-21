
let highlighted_node_id = null;

function assign_tooltip_buttons(d) {
    /**
     * Assign the functionality of tooltip buttons to refer to the specified node
     * @param d dictionary representing data bound to a specific node
     */
    let pivot_button = d3.select('#pivotButton');
    pivot_button.on('click', function() {
        let query = 'MATCH (v1)-[v2]-(v3) WHERE ID(v1)=' + d.id + ' RETURN v1, v2, v3 LIMIT 50';
        submit_query(query);
    });
    let unpin_button = d3.select('#unpinButton');
    unpin_button.on('click', function() {
        unpin_node(d)});
    let query_display_button = d3.select('#queryDisplayButton');
    query_display_button.on('click', function() {
        toggle_query_bar()});
    let query_submit_button = d3.select('.tooltipQuerySubmitButton');
    query_submit_button.on('click', function() {
        let query = get_tooltip_query();
        submit_query(query);
    })
}

function deselect_node() {
    /**
     * Deselect the currently selected node by removing the link highlight and hiding the tooltip
     */
    if(highlighted_node_id) {
        disable_highlight(highlighted_node_id);
        let node = d3.select('#node' + highlighted_node_id)
            .attr('tooltip', 'hidden');
        d3.select('.tooltipContainer')
            .style('display', 'none');
        highlighted_node_id = null;
    }
}

function get_lines_by_endpoint(endpoint_id) {
    /**
     * Given the id of a node, return an array containing two sub-arrays.
     * The first array contains all links with the endpoint ID as a source.
     * The second array contains all links with the endpoint ID as a target.
     * Used to alter color of all links connected to a specific node.
     * @return array containing two arrays of link objects
     */
    return [
        d3.selectAll('.link_line')
            .filter(function(d) {return d.source.id === endpoint_id}),
        d3.selectAll('.link_line')
            .filter(function(d) {return d.target.id === endpoint_id})]
}

function toggle_highlight(d) {
    /**
     * If the node is highlighted, run disable_highlight
     * If the node is not highlighted, run enable_highlight
     * @param d dictionary representing data bound to a specific node
     */
    if(highlighted_node_id === d.id) {  // provided node is highlighted, disable highlight
        disable_highlight(highlighted_node_id);
        highlighted_node_id = null;
    }
    else if(highlighted_node_id === null) {  // no current highlight, highlight provided node
        enable_highlight(d.id);
        highlighted_node_id = d.id;
    }
    else {  // current highlight is not provided node, clear highlight and highlight provided node
        disable_highlight(highlighted_node_id);
        enable_highlight(d.id);
        highlighted_node_id = d.id;
    }
}

function disable_highlight(id) {
    /**
     * Return links connected to the given node to their original color
     * @param id integer indicating the ID of the node to be deselected
     */
    let highlighted = get_lines_by_endpoint(id);
    highlighted[0].style('stroke', d => link_color(d));
    highlighted[1].style('stroke', d => link_color(d));
}

function enable_highlight(id) {
    /**
     * Turn links connected to the given node to the configured highlight color
     * @param id integer indicating the ID of the node to be deselected
     */
    d3.select('.node_group').select('#node' + id).select('circle')
        .transition()
        .style('box-shadow', '0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)');
    let to_highlight = get_lines_by_endpoint(id);
    to_highlight[0].style('stroke', LINK_HIGHLIGHT_COLOR);
    to_highlight[1].style('stroke', LINK_HIGHLIGHT_COLOR);
}