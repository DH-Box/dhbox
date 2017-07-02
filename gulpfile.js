var gulp = require('gulp'),
    del  = require('del'), 
    less = require('less');

// Dynamically load all other plugins.
var plugins = require("gulp-load-plugins")({
    pattern: ['gulp-*', 'gulp.*', 'main-bower-files'],
    replaceString: /\bgulp[\-.]/
});

gulp.task('clean', function () {
    del.sync(['dist']);
});

gulp.task('html', ['clean'], function () {
    gulp.src('src/templates/**/*.html')
        .pipe(gulp.dest('dist/templates'));
});

gulp.task('js', ['clean'], function () {
    var jsFiles = 'src/static/js/*.js';
    gulp.src(plugins.mainBowerFiles().concat(jsFiles))
        // .pipe(plugins.debug())
        .pipe(plugins.filter('**/*.js'))
        .pipe(plugins.debug({'title': 'js'}))
        // .pipe(plugins.uglify()
        .pipe(plugins.concat('dhbox.js'))
        // .pipe(plugins.debug({'title': 'after'}))
        .pipe(gulp.dest('dist/static/js'));
});

gulp.task('css', function () {
    var lessFiles = 'src/static/css/*.less';
    gulp.src(plugins.mainBowerFiles().concat(lessFiles))
        .pipe(plugins.filter('**/*.less'))
        .pipe(plugins.debug({'title': 'css'}))
        .pipe(plugins.less())
        .pipe(plugins.concat('dhbox.css'))
        .pipe(gulp.dest('dist/static/css'));
}); 

gulp.task('fonts', function () {
    gulp.src(plugins.mainBowerFiles().concat('src/static/fonts/*'))
        .pipe(plugins.filter('**/fonts/*.*'))
        .pipe(plugins.debug({'title': 'fonts'}))
        .pipe(gulp.dest('dist/static/fonts'));
});

gulp.task('images', ['clean'], function () {
    return gulp.src('src/static/images/*')
        .pipe(plugins.debug({'title': 'images'}))
        .pipe(gulp.dest('dist/static/images'));
});


gulp.task('other', ['clean'], function () {
    return gulp.src('src/static/*')
        .pipe(plugins.debug({'title': 'copy-other'}))
        .pipe(gulp.dest('dist/static'));
});

gulp.task('build', ['html', 'js', 'css', 'fonts', 'images', 'other'], function () {
});
