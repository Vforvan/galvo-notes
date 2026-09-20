/**
 * @file draw_svg_path.ino
 * @author Matthew Sylvester (with Gemini)
 * @brief Demonstrates the new `drawPath` command using an SVG path string.
 * * This sketch shows how to draw complex shapes defined in a standard
 * SVG 'd' path string. It draws a heart shape using lines,
 * quadratic Beziers, and a close-path command.
 */

#include <Arduino.h>
#include <XY2Galvo.h>

// Create an instance of the XY2Galvo class
XY2Galvo galvo;

// Access the library's pre-defined laser settings
extern LaserSet laser_set[];

// An SVG path string for a heart shape.
// The coordinates are in a ~100x100 unit box.

// M 10,30 Q 10,10 30,10 C 50,10 50,35 50,35
// C 50,35 50,10 70,10 Q 90,10 90,30 Q 90,50 70,70 L 50,90 L 30,70 Q 10,50 10,30 z
// A simpler one for testing:
// M 50,30 C 20,0 20,40 50,60 C 80,40 80,0 50,30 z

String logosvg[] =  {
{"M83.602539,73.267952L64.951904,84.035896L64.951904,62.5L83.602539,73.267952z"},
{"M84.602539,50L65.951904,60.767948L84.602539,71.535896L84.602539,50z"},
{"M64.951904,37.5L83.602539,48.267948L64.951904,59.0359L64.951904,37.5z"},
{"M84.602539,25L65.951904,35.767948L84.602539,46.5359L84.602539,25z"},
{"M64.951904,12.5L64.951904,34.0359L83.602539,23.26795L64.951904,12.5z"},
{"M44.30127,23.26795L62.951904,12.5L62.951904,34.0359L44.30127,23.26795z"},
{"M43.30127,21.535898L61.951904,10.767949L43.30127,0L43.30127,21.535898z"},
{"M41.30127,0L41.30127,21.535898L22.650635,10.767949L41.30127,0z"},
{"M21.650635,34.0359L21.650635,12.5L40.30127,23.26795L21.650635,34.0359z"},
{"M19.650635,12.5L19.650635,34.0359L1,23.26795L19.650635,12.5z"},
{"M0,46.5359L18.650635,35.767948L0,25L0,46.5359z"},
{"M1,48.267948L19.650635,59.0359L19.650635,37.5L1,48.267948z"},
{"M18.650635,60.767948L0,50L0,71.535896L18.650635,60.767948z"},
{"M19.650635,62.5L19.650635,84.035896L1,73.267952L19.650635,62.5z"},
{"M21.650635,62.5L21.650635,84.035896L40.30127,73.267952L21.650635,62.5z"},
{"M41.30127,96.535896L41.30127,75L22.650635,85.767952L41.30127,96.535896z"},
{"M61.951904,85.767952L43.30127,96.535896L43.30127,75L61.951904,85.767952z"},
{"M62.951904,62.5L62.951904,84.035896L44.30127,73.267952L62.951904,62.5z"},
{"M41.30127,37.017948L33.058483,32.258976L33.058483,41.776924L41.30127,37.017948z"},
{"M41.80127,36.151924L41.80127,26.633974L33.558483,31.39295L41.80127,36.151924z"},
{"M42.80127,36.151924L51.044056,31.39295L42.80127,26.633974L42.80127,36.151924z"},
{"M51.544056,41.776924L51.544056,32.258976L43.30127,37.017948L51.544056,41.776924z"},
{"M42.80127,47.401924L42.80127,37.883976L51.044056,42.642948L42.80127,47.401924z"},
{"M41.80127,49.133976L41.80127,58.651924L33.558483,53.892948L41.80127,49.133976z"},
{"M43.30127,59.517948L51.544056,54.758976L51.544056,64.276924L43.30127,59.517948z"},
{"M51.044056,65.142952L42.80127,69.901924L42.80127,60.383976L51.044056,65.142952z"},
{"M41.80127,60.383976L41.80127,69.901924L33.558483,65.142952L41.80127,60.383976z"},
{"M41.30127,59.517948L33.058483,54.758976L33.058483,64.276924L41.30127,59.517948z"},
};



void setup() {
  Serial.begin(115200);
  
  // Initialize and start the galvo worker core
  galvo.init();
  galvo.start();
  delay(100);

  Serial.println("XY2Galvo library started. Drawing SVG path demo.");

  
}

void loop() {
  // --- Set up our coordinate space ---
  // The heart path is defined in a small 100x100 (approx) coordinate space.
  // We need to scale it up and center it for the galvo.
  galvo.resetTransformation();
  
  // Scale it up significantly
  galvo.scale(300); 

  // Center it (assuming 100x100 box, 50*300=15000)
  galvo.addOffset(-15000, -10000); 

  // --- Draw the path ---
  // This single command will parse the string and send all the
  // necessary moveTo, drawTo, and drawPolyLine commands to the queue.
  // We use 30 steps to make the curves look smooth.
  int s = sizeof(logosvg) / sizeof(logosvg[0]);
  for(int i = 0; i < s; i++)
  {
    galvo.drawPath(logosvg[i].c_str(), laser_set[1], 30);
  } 
   delay(20);
}
