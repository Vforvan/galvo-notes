/**
 * @file transformations.ino
 * @author Matthew Sylvester
 * @brief Demonstrates the use of transformations for animation.
 * * This sketch draws a simple square and uses the rotate() and scale()
 * functions inside the main loop to create a continuous spinning
 * and pulsing animation. This shows how to dynamically update the
 * transformation matrix.
 */

#include <Arduino.h>
#include <XY2Galvo.h>

// Create an instance of the XY2Galvo class
XY2Galvo galvo;

// Access the library's pre-defined laser settings
extern LaserSet laser_set[];

// A simple square to be drawn and transformed
Rect square(8000, -8000, -8000, 8000);

// Variables for our animation state
float rotation_angle = 0.0;
float scale_factor = 1.0;
float scale_direction = 0.02;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  // Initialize and start the galvo worker core
  galvo.init();
  galvo.start();
  delay(100);

  Serial.println("XY2Galvo library started. Transformations demo.");
}

void loop() {
  // --- Update animation state ---
  rotation_angle += 0.05; // Increment angle for rotation
  if (rotation_angle > 2 * PI) {
    rotation_angle -= 2 * PI;
  }
  
  scale_factor += scale_direction; // Update scale for pulsing effect
  if (scale_factor > 1.5 || scale_factor < 0.5) {
    scale_direction *= -1; // Reverse scaling direction
  }
  digitalWrite(LED_BUILTIN, HIGH);
  // --- Send drawing commands with transformations ---

  // It's crucial to reset the transformation at the start of each frame.
  // Otherwise, transformations will stack on top of each other.
  galvo.resetTransformation();

  // Apply transformations. The order matters!
  // Here, we rotate first, then scale.
  galvo.rotate(rotation_angle);
  galvo.scale(scale_factor);
  
  // Now, draw the object. The transformations we just set will be
  // applied to this drawing command on the worker core.
  galvo.drawRect(square, laser_set[1]);
  digitalWrite(LED_BUILTIN, LOW);
  // Control the animation speed
  delay(20); 
}
