/*
Defines parameters for displaying nodes based on the "label" field
 */

node_types = [
    'Host',
    'Connection',
    'DNS',
    'File'
];

/**
 * Get type of node for identification in parameter functions
 * @param d dictionary representing attributes of node
 * @returns {string} indicates type of node
 */
function get_type(d) {
    return d.labels.includes('Host') ? 'Host'
        : d.labels.includes('Connection') ? 'Connection'
            : d.labels.includes('DNS') ? 'DNS'
                : d.labels.includes('File') ? 'File'
                    : 'Unknown';
}

/*
Node attribute template
function node_(d) {
    return get_type(d) === 'Host' ?
        : get_type(d) === 'Connection' ?
            : ;
}
 */

/**
 * Get radius for node type, in pixels
 * @param d dictionary representing attributes of node
 * @returns {number} radius value
 */
function node_size(d) {
    return get_type(d) === 'Host' ? 35
        : get_type(d) === 'Connection' ? 18
            : get_type(d) === 'DNS' ? 18
                : get_type(d) === 'File' ? 19
                    : 25;
}

/**
 * Get circle background color by node type
 * @param d dictionary representing attributes of node
 * @returns {string} color value
 */
function node_color(d) {
    return get_type(d) === 'Host' ? '#ffffff'
        : get_type(d) === 'Connection' ? '#515151'
            : get_type(d) === 'DNS' ? '#b13738'
                : get_type(d) === 'File' ? '#57c65c'
                    : '#141010';
}

/**
 * Get text color and opacity for node type
 * @param d dictionary representing attributes of node
 * @returns {string} rgb value specifying color and opacity
 */
function node_text_color(d) {
    return get_type(d) === 'Host' ? 'rgba(0,0,0,1)'
        : get_type(d) === 'Connection' ? 'rgb(255,255,255)'
            : get_type(d) === 'DNS' ? '#181818'
                : get_type(d) === 'File' ? '#221f21'
            : 'rgba(255,255,255,0.8)';
}

/**
 * Get configured node property to be displayed as an identification label
 * @param d dictionary representing attributes of node
 * @returns {string} identifier value
 */
function node_label(d) {
    return get_type(d) === 'Host' ? d.properties.address
        : get_type(d) === 'Connection' ? d.properties.dport
            : d.id;
}

/**
 * Get a formatted string showing all properties for a node
 * @param d dictionary representing attributes of node
 * @returns {string} formatted string
 */
function node_tooltip(d) {
    let content = get_type(d) + '<br>';
    content += 'ID: ' + d.id + '<br>';
    for (let key in d.properties) {
        content += key + ': ' + d.properties[key] + '<br>';
    }
    return content;
}