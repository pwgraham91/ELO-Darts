console.log("LOADED: base_main.js");

requirejs.config({
	paths: {
		highcharts: '/static/bower_components/highcharts/highcharts',
		jQuery: '/static/bower_components/jquery/dist/jquery.min',
		moment: '/static/bower_components/moment/min/moment.min',
		momentTimezone: '/static/bower_components/moment-timezone/builds/moment-timezone-with-data-2012-2022.min',
		underscore: '/static/bower_components/underscore/underscore-min',
		tablesorter: '/static/js/external/tablesorter/jquery.tablesorter.min'
	},
	"shim": {
		"momentTimezone": ["moment"],
		"tablesorter": ['jQuery']
	}
});

define(['/static/js/add_game.js'], function() {
});
