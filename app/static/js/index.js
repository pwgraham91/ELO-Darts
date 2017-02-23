console.log('LOADED: index.js');

define([
	'tablesorter'
], function(
	tableSorter
) {
	$('.table').tablesorter();
});
