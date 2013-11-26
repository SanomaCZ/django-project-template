({
	baseUrl: '../js/',
	paths: {
		"jquery": '../_dev/jquery-1.10.2.min'
	},
	shim: {
		"base": ['jquery']
	},
	name: '../_dev/almond',
	include: [
		"jquery",
		"base"
	],
	out: '../js/common.js',
	logLevel: 0,
	preserveLicenseComments: false
})
