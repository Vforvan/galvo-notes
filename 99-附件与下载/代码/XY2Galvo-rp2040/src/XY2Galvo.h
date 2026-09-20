#ifndef XY2Galvo_H
#define XY2Galvo_H

#include "Arduino.h"
#include <cmath>
#include <cstdint>
#include <functional>

#include "pico/multicore.h"
#include "hardware/pio.h"
#include "hardware/sync.h"
#include "hardware/gpio.h"

#include "basic_geometry.h"
#include "Queue.h"
#include "XY2-100.pio.h"
#define SCAN_MAX	0xffff
// --- Merged from standard_types.h & cdefs.h ---
//using float = float;
typedef const char* cstr;
//template<typename T> static inline T min(T a,T b) { return a<=b?a:b; }
//template<typename T> static inline T max(T a,T b) { return a>=b?a:b; }
// --- End Merged ---


// --- Merged from settings.h ---
constexpr uint32_t XY2_SM_CLOCK = 8000000;
constexpr uint32_t XY2_DATA_CLOCK = 100000;

// --- Pin Definitions ---
// The PIO program uses differential signaling for Clock, Sync, X, and Y.
// Each signal uses a pair of consecutive GPIO pins. You only need to define
// the base pin for each pair. The library and PIO will handle the second pin
// automatically (base_pin + 1).

// Differential Clock Signal
constexpr uint PIN_XY2_CLOCK      = 8;  // CLOCK+ goes here
constexpr uint PIN_XY2_CLOCK_NEG  = PIN_XY2_CLOCK + 1; // CLOCK- goes here (9)

// Differential Sync Signal (part of the clock/sync group)
constexpr uint PIN_XY2_SYNC       = 10; // SYNC+ goes here (10)
constexpr uint PIN_XY2_SYNC_NEG   = PIN_XY2_SYNC + 1;  // SYNC- goes here (11)

// Differential Y-Axis Data
constexpr uint PIN_XY2_Y          = 12; // Y+ goes here
constexpr uint PIN_XY2_Y_NEG      = PIN_XY2_Y + 1;     // Y- goes here (13)

// Differential X-Axis Data
constexpr uint PIN_XY2_X          = 14; // X+ goes here
constexpr uint PIN_XY2_X_NEG      = PIN_XY2_X + 1;     // X- goes here (15)

// Single-ended Signals
constexpr uint PIN_XY2_SYNC_XY    = 16; // Synchronization for PIO state machines
constexpr uint PIN_XY2_LASER	  = 22; // Laser ON/OFF control


constexpr int32_t SCANNER_MAX = SCAN_MAX;
constexpr float SCANNER_MAX_SWIVELS = 10000.0f / 120.0f;
constexpr float SCANNER_WIDTH = 0x10000;
constexpr float SCANNER_MAX_SPEED = SCANNER_MAX_SWIVELS * SCANNER_WIDTH / XY2_DATA_CLOCK;
// --- End Merged ---

#define PIO_XY2 pio0

struct LaserSet
{
	float speed;
	uint pattern;
	uint delay_a;	// steps to wait after start before laser ON
	uint delay_m;	// steps to wait at middle points in polygon lines
	uint delay_e;	// steps to wait with laser ON after end of line
};

// Pre-defined laser settings
static LaserSet laser_set[] =
{
	{.speed=SCANNER_MAX_SPEED, .pattern=0x003, .delay_a=0, .delay_m=0, .delay_e=20},	// 0: jump
	{.speed=SCANNER_MAX_SPEED, .pattern=0x3FF, .delay_a=0, .delay_m=6, .delay_e=0},	// 1: fast straight
	{.speed=SCANNER_MAX_SPEED*2/3, .pattern=0x3FF, .delay_a=0, .delay_m=6, .delay_e=0},	// 2: slow straight
	{.speed=SCANNER_MAX_SPEED, .pattern=0x3FF, .delay_a=0, .delay_m=0, .delay_e=0},	// 3: fast rounded
	{.speed=SCANNER_MAX_SPEED*2/3, .pattern=0x3FF, .delay_a=0, .delay_m=0, .delay_e=0},	// 4: slow rounded
};


enum DrawCmd
{
	CMD_END = 0,
	CMD_MOVETO,
	CMD_DRAWTO,
	CMD_LINETO,
	CMD_LINE,
	CMD_RECT,
	CMD_POLYLINE,
	CMD_PRINT_TEXT,
	CMD_RESET_TRANSFORMATION,
	CMD_SET_TRANSFORMATION,
    CMD_SET_TRANSFORMATION_3D,
};

union Data32
{
	DrawCmd cmd;
	const LaserSet* set;
	float f;
	uint  u;
	int   i;
	Data32(DrawCmd c) : cmd(c){}
	Data32(float f)   : f(f)  {}
	Data32(uint  u)   : u(u)  {}
	Data32(int   i)   : i(i)  {}
	Data32(const LaserSet* s) : set(s) {}
	Data32(){}
	~Data32(){}
};

enum PolyLineOptions
{
	POLYLINE_DEFAULT  = 0,
	POLYLINE_NO_START = 1,
	POLYLINE_NO_END   = 2,
	POLYLINE_INFINITE = 3,
	POLYLINE_CLOSED   = 4
};

class LaserQueue : public Queue<Data32, 4096>
{
public:
	void push (Data32 data);
	void push (const Point& p);
	void push (const Rect& r);
	Data32 pop ();
	Point pop_Point ();
	Rect pop_Rect ();
};

extern LaserQueue laser_queue;

class XY2Galvo
{
public:
	XY2Galvo();

	void init();
	void start();

    // Drawing commands
	void moveTo (const Point& dest);
	void drawTo (const Point& dest, const LaserSet&);
	void drawLine (const Point& start, const Point& dest, const LaserSet&);
	void drawRect (const Rect& rect, const LaserSet&);
	void drawRect (const Rect& rect, float rotation_rad, const LaserSet& set);
	void drawPolyLine (uint count, const Point points[], const LaserSet&, PolyLineOptions=POLYLINE_DEFAULT);
	void drawPolyLine (uint count, std::function<Point()> nextPoint, const LaserSet&, PolyLineOptions=POLYLINE_DEFAULT);
	void drawPolygon (uint count, const Point points[], const LaserSet&);
	void drawPolygon (uint count, const Point points[], float rotation_rad, const LaserSet& set);
	void drawPolygon (uint count, const Point points[], float rotation_rad, const Point& rotation_center, const LaserSet& set);
	void drawEllipse (const Rect& bbox, float angle0, uint32_t steps, const LaserSet&);
	void printText (Point start, float scale_x, float scale_y, cstr text, bool centered = false, const LaserSet& = laser_set[2], const LaserSet& = laser_set[4]);
	static void requestAbort();
    /**
     * @brief Draws a vector path defined by an SVG path string.
     * @param path_data The 'd' attribute string from an SVG <path> element.
     * @param set The LaserSet to use for all drawing operations.
     * @param tessellation_steps The number of line segments to use for approximating curves (Bézier, etc.).
     */
    void drawPath(cstr path_data, const LaserSet& set, uint tessellation_steps = 20);

    // Transformation commands
	void resetTransformation();
	void setRotation (float rad);
	void setRotationAndScale (float rad, float fx, float fy);
	void setScale (float f);
	void setScale (float fx, float fy);
	void setOffset(float dx, float dy);
	void setOffset(const Point& p) { setOffset(p.x,p.y); }
	void setOffset(const Dist& d)  { setOffset(d.dx,d.dy); }
	void setShear (float sx, float sy);
	void setProjection (float px, float py, float pz=1);
	void setTransformation (float fx, float fy, float sx, float sy, float dx, float dy);
	void setTransformation (float fx, float fy, float sx, float sy, float dx, float dy, float px, float py, float pz=1);

	void setTransformation (const Transformation& transformation);
    void pushTransformation();
    void popTransformation();
    void rotate(float rad);
    void scale(float s);
    void scale(float sx, float sy);
    void addOffset(float dx, float dy);
	const Rect WORKSPACE_BOUNDS={SCAN_MAX, -SCAN_MAX, -SCAN_MAX, SCAN_MAX};

private:

static volatile bool _abortRequest;
	static void worker();
	
	void update_transformation ();
	static uint delayed_laser_value (uint value);

	static void pio_wait_free();
	static void pio_send_data (float x, float y, uint32_t laser);
	static void send_data_blocking (const Point& p, uint32_t laser);

	static void draw_to (Point dest, float speed, uint laser_on_pattern, uint& laser_on_delay, uint end_delay);
	static void move_to (const Point& dest);
	static void line_to (const Point& dest, const LaserSet&);
	static void draw_line (const Point& start, const Point& dest, const LaserSet&);
	static void draw_rect (const Rect& rect, const LaserSet&);
	static void draw_polyline (uint count, std::function<Point()> next_point, const LaserSet&, uint flags);

	
	static void print_char (Point& textpos, float scale_x, float scale_y, const LaserSet& straight, const LaserSet& rounded, uint8_t& rmask, char c);

    // SVG Path Helpers (Core 0)
    float _parseNextFloat(char** s);
    Point _parseNextPoint(char** s, Point current, bool is_relative);
    Point _pointOnQuadraticBezier(Point p0, Point p1, Point p2, float t);
    Point _pointOnCubicBezier(Point p0, Point p1, Point p2, Point p3, float t);
    void _tessellateQuadraticBezier(Point p0, Point p1, Point p2, uint steps, const LaserSet& set);
    void _tessellateCubicBezier(Point p0, Point p1, Point p2, Point p3, uint steps, const LaserSet& set);
    void _drawPathParser(char* s, const LaserSet& set, uint steps);

    // PIO state machines
	static constexpr uint sm_laser  = 0;
	static constexpr uint sm_clock  = 1;
	static constexpr uint sm_x      = 2;
	static constexpr uint sm_y      = 3;
	
    // State variables
    static Point pos0;
    static Transformation transformation0;
    static Transformation transformation1;
    static Transformation transformation_stack[8];
    static uint transformation_stack_index;
};

#endif // XY2Galvo_H

