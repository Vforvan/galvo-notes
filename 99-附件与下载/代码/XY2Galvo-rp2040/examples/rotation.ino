/**
 * @file rotated_shapes.ino
 * @author Matthew Sylvester (with Gemini)
 * @brief Demonstrates the new overloaded drawing functions for rotated shapes.
 * * This sketch shows how to use the new `drawRect` and `drawPolygon`
 * functions that take a rotation angle as an argument, without
 * needing to use the full transformation stack.
 */

#include <Arduino.h>
#include <XY2Galvo.h>

// Create an instance of the XY2Galvo class
XY2Galvo galvo;

// Access the library's pre-defined laser settings
extern LaserSet laser_set[];

// A simple square to be drawn
Rect square(8000, -8000, -8000, 8000);

// A simple triangle to be drawn
Point triangle[3] = {
  {0, 10000},
  {-8660, -5000},
  {8660, -5000}
};

float rotation = 0.0;

void setup() {
  Serial.begin(115200);
  
  // Initialize and start the galvo worker core
  galvo.init();
  galvo.start();
  delay(100);

  Serial.println("XY2Galvo library started. Rotated shapes demo.");
}

void loop() {
  // Update rotation angle
  rotation += 0.05;
  if (rotation > 2 * PI) {
    rotation -= 2 * PI;
  }

  // --- Draw a rotated rectangle ---
  // This will draw the 'square' Rect, rotated by 'rotation' radians
  // around its own center.
  galvo.drawRect(square, rotation, laser_set[1]);

  
  // --- Draw a rotated polygon ---
  // We'll move the triangle to the right so it doesn't overlap
  Point triangle_center(20000, 0);

  // This will draw the 'triangle' polygon, rotated by '-rotation' radians
  // around the 'triangle_center' point.
  // Note: We are using the transformation stack here just to move the
  // center point, but the rotation itself is handled by the new function.
  galvo.pushTransformation();
  galvo.addOffset(triangle_center.x, triangle_center.y);
  galvo.drawPolygon(3, triangle, -rotation, Point(0,0), laser_set[2]);
  galvo.popTransformation();
  

  // Control the animation speed
  delay(20); 
}
