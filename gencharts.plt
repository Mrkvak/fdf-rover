set datafile separator ',';
set terminal png font 'Verdana,12' size 1280,720;

set xdata time;
set timefmt "%Y-%m-%d %H:%M:%S";
set y2tics

set key autotitle columnhead;
set title filename

set output filename."-speed-spm.png"
set ylabel "speed [s/500m]"
set y2label "spm [1/min]"
plot filename using 1:5 with lines lw 2, '' using 1:6 with lines lw 2 axes x1y2;


set output filename."-distance-cals.png"
set ylabel "distance [m]"
set y2label "calories [kcal]"
plot filename using 1:8 with lines lw 2, '' using 1:9 with lines lw 2 axes x1y2;

set output filename."-spm-heartrate.png"
set ylabel "spm [1/min]"
set y2label "heart rate [bpm]"
plot filename using 1:6 with lines lw 2, '' using 1:4 with lines lw 2 axes x1y2;

set output filename."-spm-power.png"
set ylabel "spm [1/min]"
set y2label "power [W]"
plot filename using 1:6 with lines lw 2, '' using 1:7 with lines lw 2 axes x1y2;

