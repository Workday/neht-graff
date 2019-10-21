/*
Defines parameters for displaying links based on the "type" field
 */

link_types = [
    'ORIG',
    'RESP'
];

/**
 * Get link line color by relationship type
 * @param d
 * @returns {string}
 */
function link_color(d) {
    return d.type === 'ORIG' ? '#3f7bff'
        : d.type === 'RESP' ? '#ff9a34'
            : '#808080';
}

