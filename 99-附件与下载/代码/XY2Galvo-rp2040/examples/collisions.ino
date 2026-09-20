/**
 * @file draw_svg_path.ino
 * @author Matthew Sylvester 
 * @brief Demonstrates the ability to assess intersections of rectangles
 */

#include <Arduino.h>
#include <XY2Galvo.h>

// Create an instance of the XY2Galvo class
XY2Galvo galvo;

// Access the library's pre-defined laser settings
extern LaserSet laser_set[];

struct RectVector
{
  Rect rect;          //the displayed object
  Dist vector;          //its motion vector, moves this far on each update
  float rad;              //its present angle
  float angularvelocity;     //added to the present angle each update
};

const int numRect = 30;
RectVector collection[numRect];

uint16_t wallwidth = 2048;        //create rectangles to act as the walls
float galvoscale = 300;
float maximum = 0xffff/galvoscale/2;
Rect right({maximum, maximum}, {maximum + wallwidth,-maximum});
Rect top({-maximum, maximum + wallwidth}, {maximum ,maximum});
Rect bottom({-maximum, -maximum}, {maximum ,-maximum - wallwidth});
Rect left({-maximum - wallwidth, maximum}, {-maximum ,-maximum});


void setup() {
  Serial.begin(115200);
  
  // Initialize and start the galvo worker core
  galvo.init();
  galvo.start();
  delay(100);
  randomSeed(analogRead(3) * millis());
  Serial.println("XY2Galvo library started. Drawing SVG path demo.");
  for(int i = 0; i < numRect; i++)    //initialize to random sizes, angles, motion vectors adn angular rate
  {
    collection[i].rect = Rect({random(-100.0, -1000.0)/100.0, random(100.0, 1000.0)/100.0}, {random(100.0,1000.0)/100.0, random(-100.0, -1000.0)/100.0} ); 
    Dist displacement(random(-5000.0, 5000.0)/100.0, random(-5000.0, 5000.0)/100.0 );
    
    collection[i].rect = collection[i].rect + displacement;
    Dist motion(random(-300.0, 300.0)/100.0, random(-300.0, 300.0)/100.0 ); 
    collection[i].vector = motion;

    collection[i].rad = (float)random(-1000, 1000)/1000.0;
    collection[i].angularvelocity = (float)random(-1000, 1000)/10000.0;
  }

}

Rect rect({-20, 20},{20, -20});
Dist vec(0.3,0.3);

void loop() {

  galvo.resetTransformation();
  galvo.scale(galvoscale); 

  for(int i = 0; i < numRect; i++)
  {
    if(intersects(collection[i].rect, top) || intersects(collection[i].rect, bottom))   //check for intersections with the edge of teh workspace
    {
      collection[i].vector = {collection[i].vector.dx, -collection[i].vector.dy};   //if intersects, flip the magnitude of the appropriate component of the mnotion vector
    }
    else if(intersects(collection[i].rect, right) || intersects(collection[i].rect, left))
    {
      collection[i].vector = {-collection[i].vector.dx, collection[i].vector.dy};
    }

    galvo.drawRect(collection[i].rect,collection[i].rad, laser_set[2]);     //draw it
    collection[i].rect = collection[i].rect + collection[i].vector;         //update its position adn its angle for the next update
    collection[i].rad += collection[i].angularvelocity;
  }
   delay(10);
}
