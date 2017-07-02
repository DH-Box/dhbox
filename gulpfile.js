var gulp = require('gulp'),
    del  = require('del')

// Dynamically load plugins.
var plugins = require("gulp-load-plugins")({
	pattern: ['gulp-*', 'gulp.*', 'main-bower-files'],
	replaceString: /\bgulp[\-.]/
});

var dest = 'dist/'

gulp.task('clean', function () {
    del.sync(['dist']);
});

gulp.task('useref', ['clean'], function () {
    var assets = useref.assets();

    return gulp.src(['src/**/*.html', '!src/static/bower_components/**'])
        .pipe(assets)
        .pipe(gulpif('*.js', uglify()))
        .pipe(gulpif('*.css', less()))
        .pipe(assets.restore())
        .pipe(useref())
        .pipe(gulp.dest('dist'))
});

gulp.task('js', function () { 
	var jsFiles = 'src/static/js/*.js'
	gulp.src(plugins.mainBowerFiles().concat(jsFiles))
	.pipe(plugins.filter('*.js'))
	//.pipe(plugins.concat('main.js'))
	//.pipe(plugins.uglify())
	.pipe(gulp.dest('dist/static/js'));
});

gulp.task('css', function () { 
	var lessFiles = 'src/static/css/*.less'
	gulp.src(plugins.mainBowerFiles().concat(lessFiles))
        .pipe(plugins.if('*.less', plugins.less()))
	.pipe(plugins.concat('dhbox.css'))
	.pipe(gulp.dest(dest + 'css'));
}); 

gulp.task('copy-static', ['copy-images', 'copy-fonts', 'copy-other'], function () {

});

gulp.task('copy-images', ['clean'], function () {
    return gulp.src('src/static/images/*')
        .pipe(gulp.dest('dist/static/images'));
});

gulp.task('copy-fonts', ['clean'], function () {
    return gulp.src('src/static/fonts/*')
        .pipe(gulp.dest('dist/static/fonts'));
});


gulp.task('copy-other', ['clean'], function () {
    return gulp.src('src/static/*')
        .pipe(gulp.dest('dist/static'));
});


gulp.task('build', ['copy-static', 'useref'], function () {

});
