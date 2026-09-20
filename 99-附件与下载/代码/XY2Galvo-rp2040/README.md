# XY2Galvo Library for Raspberry Pi Pico
This is an Arduino library for controlling XY2-100 protocol-based laser galvanometers using the RP2040's Programmable I/O (PIO) feature. It's designed to be efficient and provide a simple API for drawing vector graphics.
This library is largely based on the excellent work done by [MegaTokio](https://github.com/Megatokio) in his [Laseroids](https://github.com/Megatokio/Laseroids) project.

## Features
PIO-based signal generation: Generates the precise, high-speed differential signals for CLOCK, SYNC, X, and Y required by the XY2-100 protocol.

Dual-core operation: Offloads the demanding signal generation and drawing logic to the second core (core1), leaving the main loop (core0) free for your application logic.

Command Queue: Uses a queue to send drawing commands from your main application to the drawing core.

Transformation Matrix: Supports affine transformations (scaling, rotation, translation) to manipulate your drawings.

## Installation

### Platformio
simply add this git repo to the `lib_deps` line in `platformio.ini`
### Arduino
Download the latest release of this library from the GitHub repository. (Remember to update this link!)

In the Arduino IDE, go to Sketch -> Include Library -> Add .ZIP Library... and select the downloaded file.

Restart the Arduino IDE.

## Hardware Setup
The library requires a specific pinout to work with the PIO programs. The differential signals each require a pair of consecutive GPIO pins. You only need to define the base pin for each pair in the code.

`CLOCK`: `GPIO8` (CLOCK+) & `GPIO9` (CLOCK-)

`SYNC`: `GPIO10` (SYNC+) & `GPIO11` (SYNC-)

`Y-Axis`: `GPIO12` (Y+) & `GPIO13` (Y-)

`X-Axis`: `GPIO14` (X+) & `GPIO15` (X-)

`PIO SYNC`: `GPIO16` (Internal synchronization between state machines)

`LASER`: `GPIO22` (Laser enable/modulation signal)

## Drawing Commands
`moveTo(Point dest)`: Moves the scanner to a destination point with the laser off.

`drawTo(Point dest, const LaserSet& set)`: Draws a line from the current position to a destination.

`drawLine(Point start, Point dest, const LaserSet& set)`: Moves to a start point and then draws a line to the destination.

`drawRect(const Rect& rect, const LaserSet& set)`: Draws a rectangle.

`drawPolyLine(uint count, const Point points[], const LaserSet& set, PolyLineOptions flags)`: Draws a series of connected lines.

`drawPolygon(uint count, const Point points[], const LaserSet& set)`: Draws a closed polygon.

## Transformations
`resetTransformation()`: Resets all transformations.

`setTransformation(const Transformation& t)`: Applies a full transformation matrix.

`rotate(float rad)`: Rotates the drawing context.

`scale(float s)`: Scales the drawing context uniformly.

`scale(float sx, float sy)`: Scales the drawing context non-uniformly.

`addOffset(float dx, float dy)`: Translates (moves) the drawing context.

## License
This library is licensed under the BSD 3-Clause License. See the LICENSE file for details.
