var gulp = require('gulp'),
    useref = require('gulp-useref'),
    gulpif = require('gulp-if'),
    uglify = require('gulp-uglify'),
    minifyCss = require('gulp-minify-css'),
    del = require('del'),
    less = require('gulp-less');

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