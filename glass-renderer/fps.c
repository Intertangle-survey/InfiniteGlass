#include <stdlib.h>
#include <sys/time.h>
#import "wm.h"

unsigned long get_timestamp() {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return 1000000 * tv.tv_sec + tv.tv_usec;
}

unsigned long frames = 0;
unsigned long epoch = 0;
unsigned long start_time = 0;
unsigned long total_time = 0;

void draw_fps_start() {
  start_time = get_timestamp();
}


void draw_fps() {
  unsigned long now = get_timestamp();
  total_time += now - start_time;
  
  frames++;
  if (now - epoch >= 2000000) { // 10 Seconds
    fprintf(eventlog,
           "FPS: %f frames/sec, %f sec/frame\n",
            (float) frames * (float) 1000000 / (float) (now - epoch), (float) total_time / 1000000. / (float) frames);
    epoch = now;
    frames = 0;
    total_time = 0;
  }
}
