#include "XY2Galvo.h"
#include <cctype>   // For isalpha, isspace
#include <stdlib.h> // For strtof
#include <cstring>
#include "vt_vector_font.h"

volatile bool XY2Galvo::_abortRequest = false;

// --- Global state for the library ---
LaserQueue laser_queue;
Point XY2Galvo::pos0;
Transformation XY2Galvo::transformation0;
Transformation XY2Galvo::transformation1;
Transformation XY2Galvo::transformation_stack[8];
uint XY2Galvo::transformation_stack_index = 0;

static volatile bool core1_running = false;
static volatile bool core1_suspend = false;
static volatile bool core1_suspended = false;

static uint laser_delay_queue[16] = {0};
static uint laser_delay_size = 14; // From LASER_QUEUE_DELAY
static uint laser_delay_index = 0;

#define NELEM(feld) (sizeof(feld) / sizeof((feld)[0])) // UNSIGNED !!

static uint32_t vt_font_col1[256]; // index in vt_font_data[]
static int8_t vt_font_width[256];  // character print width (including +1 for line width but no spacing)

static void vt_init_vector_font()
{
    for (uint i = 0, c = ' '; c < NELEM(vt_font_col1) && i < NELEM(vt_font_data); c++)
    {
        vt_font_col1[c] = i;
        i += 2; // left-side mask and right-side mask

        int8_t width = 0;
        while (vt_font_data[i++] > E)
        {
            while (vt_font_data[i] < E)
            {
                width = max(width, vt_font_data[i]);
                i += 2;
            }
        }
        vt_font_width[c] = width + 1;

        assert(vt_font_data[i - 1] == E);
    }
}

// --- LaserQueue Implementation ---
void LaserQueue::push(Data32 data)
{
    while (!free())
    {
        tight_loop_contents();
    } // Wait for space
    putc(data);
}
void LaserQueue::push(const Point &p)
{
    push(p.x);
    push(p.y);
}
void LaserQueue::push(const Rect &r)
{
    push(r.top_left());
    push(r.bottom_right());
}
Data32 LaserQueue::pop()
{
    while (!avail())
    {
        tight_loop_contents();
    } // Wait for data
    return getc();
}
Point LaserQueue::pop_Point()
{
    float x = pop().f;
    float y = pop().f;
    return Point(x, y);
}
Rect LaserQueue::pop_Rect()
{
    Point p1 = pop_Point();
    Point p2 = pop_Point();
    return Rect(p1, p2);
}

// --- XY2Galvo Class Implementation ---

XY2Galvo::XY2Galvo() {}

void XY2Galvo::init()
{
    _abortRequest = false;
    uint mask = (1u << PIN_XY2_LASER) | (1u << PIN_XY2_SYNC_XY) | (3u << PIN_XY2_CLOCK) | (3u << PIN_XY2_SYNC) | (3u << PIN_XY2_X) | (3u << PIN_XY2_Y);
    pio_sm_set_pins_with_mask(PIO_XY2, sm_x, ~(1u << PIN_XY2_LASER), mask);
    pio_sm_set_pindirs_with_mask(PIO_XY2, sm_x, -1u, mask);
    for (uint i = 0; i < 32; i++)
    {
        if (mask & (1u << i))
            pio_gpio_init(PIO_XY2, i);
    }

    // Init PIO state machines
    uint offset = pio_add_program(PIO_XY2, &xy2_clock_program);
    pio_sm_config c = xy2_clock_program_get_default_config(offset);
    sm_config_set_sideset_pins(&c, PIN_XY2_CLOCK);
    sm_config_set_clkdiv(&c, float(F_CPU) / XY2_SM_CLOCK);
    pio_sm_init(PIO_XY2, sm_clock, offset + xy2_clock_offset_start, &c);

    offset = pio_add_program(PIO_XY2, &xy2_data_program);
    c = xy2_data_program_get_default_config(offset);
    sm_config_set_clkdiv(&c, float(F_CPU) / XY2_SM_CLOCK);
    sm_config_set_out_shift(&c, false, false, 32);
    sm_config_set_fifo_join(&c, PIO_FIFO_JOIN_TX);
    sm_config_set_jmp_pin(&c, PIN_XY2_SYNC_XY);

    sm_config_set_sideset_pins(&c, PIN_XY2_X);
    pio_sm_init(PIO_XY2, sm_x, offset + xy2_data_offset_start, &c);

    sm_config_set_sideset_pins(&c, PIN_XY2_Y);
    pio_sm_init(PIO_XY2, sm_y, offset + xy2_data_offset_start, &c);

    offset = pio_add_program(PIO_XY2, &xy2_laser_program);
    c = xy2_laser_program_get_default_config(offset);
    sm_config_set_clkdiv(&c, float(F_CPU) / XY2_SM_CLOCK);
    sm_config_set_out_shift(&c, true, false, 10);
    sm_config_set_fifo_join(&c, PIO_FIFO_JOIN_TX);
    sm_config_set_mov_status(&c, STATUS_TX_LESSTHAN, 1);
    sm_config_set_out_pins(&c, PIN_XY2_LASER, 1);
    sm_config_set_sideset_pins(&c, PIN_XY2_SYNC_XY);
    pio_sm_init(PIO_XY2, sm_laser, offset + xy2_laser_offset_start, &c);

    // gpio_set_outover(PIN_XY2_LASER, GPIO_OVERRIDE_INVERT);
    gpio_set_outover(PIN_XY2_LASER, GPIO_OVERRIDE_NORMAL); // un-invert laser control signal
    vt_init_vector_font();
}

void XY2Galvo::requestAbort()
{
     _abortRequest = true; 
}

void XY2Galvo::start()
{
    if (!core1_running)
    {
        multicore_launch_core1(XY2Galvo::worker);
    }
    while (!core1_running)
    {
        tight_loop_contents();
    }
}

__attribute__((noreturn)) void XY2Galvo::worker()
{
    core1_running = true;

    pio_sm_set_enabled(PIO_XY2, sm_laser, false);
    pio_sm_set_enabled(PIO_XY2, sm_clock, false);
    pio_sm_set_enabled(PIO_XY2, sm_x, false);
    pio_sm_set_enabled(PIO_XY2, sm_y, false);

    pio_sm_clear_fifos(PIO_XY2, sm_laser);
    pio_sm_clear_fifos(PIO_XY2, sm_x);
    pio_sm_clear_fifos(PIO_XY2, sm_y);

    pio_enable_sm_mask_in_sync(PIO_XY2, (1u << sm_clock) | (1u << sm_x) | (1u << sm_y) | (1u << sm_laser));

    memset(laser_delay_queue, 0, sizeof(laser_delay_queue));
    pio_send_data(0.0f, 0.0f, 0x000);

    for (;;)
    {
        if (_abortRequest)
        {
            // Core 1 owns the queue, so it can safely clear it
            while (laser_queue.avail())
                laser_queue.pop();

            // Turn off laser
            

            _abortRequest = false;
        }
        DrawCmd cmd = laser_queue.pop().cmd;
        switch (cmd)
        {
        case CMD_MOVETO:
        {
            Point p1 = laser_queue.pop_Point();
            move_to(p1);
            break;
        }
        case CMD_DRAWTO:
        {
            const LaserSet *set = laser_queue.pop().set;
            Point p1 = laser_queue.pop_Point();
            uint laser_on_delay = 0;
            draw_to(p1, set->speed, set->pattern, laser_on_delay, set->delay_m);
            break;
        }
        case CMD_LINETO:
        {
            const LaserSet *set = laser_queue.pop().set;
            Point p1 = laser_queue.pop_Point();
            line_to(p1, *set);
            break;
        }
        case CMD_LINE:
        {
            const LaserSet *set = laser_queue.pop().set;
            Point p1 = laser_queue.pop_Point();
            Point p2 = laser_queue.pop_Point();
            draw_line(p1, p2, *set);
            break;
        }
        case CMD_RECT:
        {
            const LaserSet *set = laser_queue.pop().set;
            Rect rect = laser_queue.pop_Rect();
            draw_rect(rect, *set);
            break;
        }
        case CMD_POLYLINE:
        {
            const LaserSet *set = laser_queue.pop().set;
            uint flags = laser_queue.pop().u;
            uint count = laser_queue.pop().u;
            draw_polyline(count, []()
                          { return laser_queue.pop_Point(); }, *set, flags);
            break;
        }
        case CMD_PRINT_TEXT: // 	2*LaserSet, Point, 2*float, n*char, 0
        {
            const LaserSet *straight = laser_queue.pop().set;
            const LaserSet *rounded = laser_queue.pop().set;
            Point start = laser_queue.pop_Point();
            float scale_x = laser_queue.pop().f;
            float scale_y = laser_queue.pop().f;

            uint8_t rmask = 0;
            while (char c = char(laser_queue.pop().u))
            {
                print_char(start, scale_x, scale_y, *straight, *rounded, rmask, c);
            }
            continue;
        }

        case CMD_RESET_TRANSFORMATION:
        {
            transformation1.reset();
            break;
        }
        case CMD_SET_TRANSFORMATION:
        {
            while (laser_queue.avail() < 6)
            {
            }
            Data32 *dest = reinterpret_cast<Data32 *>(&transformation1);
            laser_queue.read(dest, 6);
            transformation1.is_projected = false;
            break;
        }
        case CMD_SET_TRANSFORMATION_3D:
        {
            while (laser_queue.avail() < 9)
            {
            }
            Data32 *dest = reinterpret_cast<Data32 *>(&transformation1);
            laser_queue.read(dest, 9);
            transformation1.is_projected = true;
            break;
        }
        case CMD_END:
        default:
            // Do nothing, loop
            break;
        }
    }
}

// --- Core Drawing Logic (runs on Core 1) ---

uint XY2Galvo::delayed_laser_value(uint value)
{
    if (laser_delay_index >= laser_delay_size)
        laser_delay_index = 0;
    std::swap(value, laser_delay_queue[laser_delay_index++]);
    return value;
}

void XY2Galvo::pio_wait_free()
{
    while (pio_sm_is_tx_fifo_full(PIO_XY2, sm_x))
    {
        tight_loop_contents();
    }
}

void XY2Galvo::pio_send_data(float x, float y, uint32_t laser)
{
    pos0.x = x;
    pos0.y = y;
    laser = delayed_laser_value(laser);

    uint32_t ix = 0x8000 + int32_t(x);
    uint32_t iy = 0x8000 - int32_t(y);
    if (ix >> 16)
        ix = int32_t(ix) < 0 ? 0 : 0xffff;
    if (iy >> 16)
        iy = int32_t(iy) < 0 ? 0 : 0xffff;

    pio_sm_put_blocking(PIO_XY2, sm_x, ix);
    pio_sm_put_blocking(PIO_XY2, sm_y, iy);
    pio_sm_put_blocking(PIO_XY2, sm_laser, laser);
}

void XY2Galvo::send_data_blocking(const Point &p, uint32_t laser)
{
    pio_wait_free();
    pio_send_data(p.x, p.y, laser);
}

void __not_in_flash_func(XY2Galvo::draw_to)(Point dest, float speed, uint laser_on_pattern, uint &laser_on_delay, uint end_delay)
{
    transformation1.transform(dest);
    Dist dist = dest - pos0;
    float line_length = dist.length();
    if (line_length == 0)
        return;
    Dist step = dist * (speed / line_length);

    uint laser_off_pattern = laser_set[0].pattern;

    while (line_length > speed)
    {
        line_length -= speed;
        uint current_pattern = (laser_on_delay > 0) ? laser_off_pattern : laser_on_pattern;
        send_data_blocking(pos0 + step, current_pattern);
        if (laser_on_delay > 0)
            laser_on_delay--;
    }

    if (pos0 != dest)
    {
        uint current_pattern = (laser_on_delay > 0) ? laser_off_pattern : laser_on_pattern;
        send_data_blocking(dest, current_pattern);
        if (laser_on_delay > 0)
            laser_on_delay--;
    }

    for (uint i = 0; i < end_delay; i++)
    {
        uint current_pattern = (laser_on_delay > 0) ? laser_off_pattern : laser_on_pattern;
        send_data_blocking(dest, current_pattern);
        if (laser_on_delay > 0)
            laser_on_delay--;
    }
}

void XY2Galvo::move_to(const Point &dest) { line_to(dest, laser_set[0]); }

void XY2Galvo::line_to(const Point &dest, const LaserSet &set)
{
    uint laser_on_delay = set.delay_a;
    draw_to(dest, set.speed, set.pattern, laser_on_delay, set.delay_e);
}

void XY2Galvo::draw_line(const Point &start, const Point &dest, const LaserSet &set)
{
    move_to(start);
    line_to(dest, set);
}

void XY2Galvo::draw_rect(const Rect &bbox, const LaserSet &set)
{
    move_to(bbox.top_left());
    line_to(bbox.top_right(), set);
    line_to(bbox.bottom_right(), set);
    line_to(bbox.bottom_left(), set);
    line_to(bbox.top_left(), set);
}

void XY2Galvo::drawEllipse(const Rect &bbox, float angle, uint32_t steps, const LaserSet &set)
{
    const Point center = bbox.center();
    float fx = bbox.width() / 2;
    float fy = bbox.height() / 2;

    float step = 2 * PI / (float)(steps);

    drawPolyLine(steps, [center, fx, fy, step, &angle]()
                 {
		float a = angle;
		angle += step;
		return center + Dist(fx*cos(a),fy*sin(a)); }, set, POLYLINE_CLOSED);
}

void XY2Galvo::setRotation(float rad) // and reset scale and shear
{
    transformation0.setRotation(rad);
    update_transformation();
}

void XY2Galvo::setScale(float f)
{
    transformation0.setScale(f);
    update_transformation();
}

void XY2Galvo::setScale(float fx, float fy)
{
    transformation0.setScale(fx, fy);
    update_transformation();
}

void XY2Galvo::setOffset(float dx, float dy)
{
    transformation0.setOffset(dx, dy);
    update_transformation();
}

void XY2Galvo::setShear(float sx, float sy)
{
    transformation0.setShear(sx, sy);
    update_transformation();
}

void XY2Galvo::setProjection(float px, float py, float pz)
{
    transformation0.setProjection(px, py, pz);
    update_transformation();
}

void XY2Galvo::setRotationAndScale(float rad, float fx, float fy)
{
    transformation0.setRotationAndScale(rad, fx, fy);
    update_transformation();
}

void __not_in_flash_func(XY2Galvo::draw_polyline)(uint count, std::function<Point()> next_point, const LaserSet &set, uint flags)
{
    bool closed = flags == POLYLINE_CLOSED;
    bool no_start = flags & POLYLINE_NO_START;
    bool no_end = flags & POLYLINE_NO_END;

    Point start;
    if (!no_start && count > 0)
    {
        count--;
        start = next_point();
        move_to(start);
    }
    if (count == 0)
        return;

    uint laser_on_delay = no_start ? 0 : set.delay_a;
    uint delay = set.delay_m;

    while (count > 0)
    {
        count--;
        Point dest = next_point();
        if (count == 0 && !no_end)
            delay = set.delay_e;
        draw_to(dest, set.speed, set.pattern, laser_on_delay, delay);
    }

    if (closed)
        draw_to(start, set.speed, set.pattern, laser_on_delay, set.delay_e);
}

// --- Public API methods (run on Core 0) ---

void XY2Galvo::moveTo(const Point &p)
{
    laser_queue.push(CMD_MOVETO);
    laser_queue.push(p);
}
void XY2Galvo::drawTo(const Point &p, const LaserSet &set)
{
    laser_queue.push(CMD_DRAWTO);
    laser_queue.push(&set);
    laser_queue.push(p);
}
void XY2Galvo::drawLine(const Point &p1, const Point &p2, const LaserSet &set)
{
    laser_queue.push(CMD_LINE);
    laser_queue.push(&set);
    laser_queue.push(p1);
    laser_queue.push(p2);
}
void XY2Galvo::drawRect(const Rect &rect, const LaserSet &set)
{
    laser_queue.push(CMD_RECT);
    laser_queue.push(&set);
    laser_queue.push(rect);
}

// NEW FUNCTION: Overload for rotated drawRect
// Rotates the rect around its own center.
void XY2Galvo::drawRect(const Rect &rect, float rotation_rad, const LaserSet &set)
{
    if (rotation_rad == 0.0f)
    {
        drawRect(rect, set); // Call the original, fast CMD_RECT version
        return;
    }

    Point center = rect.center();
    Point corners[4] = {
        rect.top_left(),
        rect.top_right(),
        rect.bottom_right(),
        rect.bottom_left()};

    Point rotated_corners[4];
    float sin_r = sin(rotation_rad);
    float cos_r = cos(rotation_rad);

    for (int i = 0; i < 4; i++)
    {
        Dist d = corners[i] - center;
        d.rotate(sin_r, cos_r); // Use the sin/cos version for efficiency
        rotated_corners[i] = center + d;
    }

    // Send as a closed polyline
    drawPolyLine(4, rotated_corners, set, POLYLINE_CLOSED);
}

void XY2Galvo::drawPolyLine(uint count, const Point points[], const LaserSet &set, PolyLineOptions flags)
{
    laser_queue.push(CMD_POLYLINE);
    laser_queue.push(&set);
    laser_queue.push(uint(flags));
    laser_queue.push(count);
    for (uint i = 0; i < count; i++)
        laser_queue.push(points[i]);
}
void XY2Galvo::drawPolyLine(uint count, std::function<Point()> nextPoint, const LaserSet &set,
                            PolyLineOptions flags)
{
    laser_queue.push(CMD_POLYLINE);
    laser_queue.push(&set);
    laser_queue.push(flags);
    laser_queue.push(count);
    for (uint i = 0; i < count; i++)
        laser_queue.push(nextPoint());
}

void XY2Galvo::drawPolygon(uint count, const Point points[], const LaserSet &set)
{
    drawPolyLine(count, points, set, POLYLINE_CLOSED);
}

// NEW FUNCTION: Overload for rotated drawPolygon (defaults to rotating around 0,0)
void XY2Galvo::drawPolygon(uint count, const Point points[], float rotation_rad, const LaserSet &set)
{
    // Default to rotating around origin (0,0)
    drawPolygon(count, points, rotation_rad, Point(0, 0), set);
}

// NEW FUNCTION: Overload for rotated drawPolygon with a specific center
void XY2Galvo::drawPolygon(uint count, const Point points[], float rotation_rad, const Point &rotation_center, const LaserSet &set)
{
    if (rotation_rad == 0.0f)
    {
        drawPolygon(count, points, set); // Call original
        return;
    }
    if (count == 0)
        return;

    // This function runs on Core 0, so dynamic allocation is safe.
    Point *rotated_points = new Point[count];
    if (!rotated_points)
        return; // Allocation failed

    float sin_r = sin(rotation_rad);
    float cos_r = cos(rotation_rad);

    for (uint i = 0; i < count; i++)
    {
        Dist d = points[i] - rotation_center;
        d.rotate(sin_r, cos_r);
        rotated_points[i] = rotation_center + d;
    }

    drawPolygon(count, rotated_points, set); // This calls the original polygon function

    delete[] rotated_points;
}

void XY2Galvo::update_transformation()
{
    static_assert(sizeof(Data32) == sizeof(float), "Size mismatch");
    laser_queue.push(transformation0.is_projected ? CMD_SET_TRANSFORMATION_3D : CMD_SET_TRANSFORMATION);
    uint n = transformation0.is_projected ? 9 : 6;
    while (laser_queue.free() < n)
    {
        tight_loop_contents();
    }
    Data32 *data = reinterpret_cast<Data32 *>(&transformation0);
    laser_queue.write(data, n);
}

void XY2Galvo::resetTransformation()
{
    transformation0.reset();
    laser_queue.push(CMD_RESET_TRANSFORMATION);
}

void XY2Galvo::setTransformation(const Transformation &t)
{
    transformation0 = t;
    update_transformation();
}

void XY2Galvo::setTransformation(float fx, float fy, float sx, float sy, float dx, float dy)
{
    new (&transformation0) Transformation(fx, fy, sx, sy, dx, dy);
    update_transformation();
}

void XY2Galvo::setTransformation(float fx, float fy, float sx, float sy, float dx, float dy, float px, float py, float pz)
{
    new (&transformation0) Transformation(fx, fy, sx, sy, dx, dy, px, py, pz);
    update_transformation();
}

void XY2Galvo::pushTransformation()
{
    transformation_stack[--transformation_stack_index & 7] = transformation0;
}

void XY2Galvo::popTransformation()
{
    transformation0 = transformation_stack[transformation_stack_index++ & 7];
    update_transformation();
}
void XY2Galvo::rotate(float rad)
{
    transformation0.rotate(rad);
    update_transformation();
}
void XY2Galvo::scale(float s)
{
    transformation0.scale(s);
    update_transformation();
}
void XY2Galvo::scale(float sx, float sy)
{
    transformation0.scale(sx, sy);
    update_transformation();
}
void XY2Galvo::addOffset(float dx, float dy)
{
    transformation0.addOffset(dx, dy);
    update_transformation();
}

float printWidth(cstr s)
{
    // calculate print width for string
    // as printed by drawing command DrawText

    int width = 0;
    uint8_t mask = 0;

    while (uint8_t c = uint8_t(*s++))
    {
        width += vt_font_width[c];
        int8_t *p = vt_font_data + vt_font_col1[c];
        if (mask & uint8_t(*p))
            width++;              // +1 if glyphs would touch
        mask = uint8_t(*(p + 1)); // remember for next
    }
    return float(width);
}

void XY2Galvo::printText(Point start, float scale_x, float scale_y, cstr text, bool centered,
                         const LaserSet &straight, const LaserSet &rounded)
{
    // CMD_PRINT_TEXT, 2*LaserSet, Point, 2*float, n*char, 0

    if (centered)
        start.x -= printWidth(text) * scale_x / 2;

    laser_queue.push(CMD_PRINT_TEXT);
    laser_queue.push(&straight);
    laser_queue.push(&rounded);
    laser_queue.push(start);
    laser_queue.push(scale_x);
    laser_queue.push(scale_y);
    char c;
    do
    {
        laser_queue.push(c = *text++);
    } while (c);
}

void XY2Galvo::print_char(Point &p0, float scale_x, float scale_y, const LaserSet &straight, const LaserSet &rounded, uint8_t &rmask, char c)
{
    int8_t *p = vt_font_data + vt_font_col1[(uint8_t)c];

    uint lmask = uint8_t(*p++);
    if (rmask & lmask)
        p0.x += scale_x;   // apply kerning
    rmask = uint8_t(*p++); // for next kerning

    while (*p != E)
    {
        int line_type = *p++;

        const LaserSet &set = line_type == L ? straight : rounded;

        Point pt;
        pt.x = p0.x + *p++ * scale_x;
        pt.y = p0.y + *p++ * scale_y;
        move_to(pt);

        uint delay_a = set.delay_a;
        while (*p < E)
        {
            pt.x = p0.x + *p++ * scale_x;
            pt.y = p0.y + *p++ * scale_y;
            draw_to(pt, set.speed, set.pattern, delay_a, *p < E ? set.delay_m : set.delay_e);
        }
    }

    p0.x += vt_font_width[(uint8_t)c] * scale_x; // update print position
}

// --- NEW SVG Path Implementation (Core 0) ---

/**
 * @brief Helper to parse the next float from a string, advancing the pointer.
 * Skips leading whitespace and commas.
 */
float XY2Galvo::_parseNextFloat(char **s)
{
    // Skip whitespace, newlines, and commas
    while (**s == ' ' || **s == '\t' || **s == '\n' || **s == '\r' || **s == ',')
    {
        (*s)++;
    }
    char *end;
    float val = strtof(*s, &end);
    *s = end;
    return val;
}

/**
 * @brief Helper to parse the next point (x, y) from a string.
 */
Point XY2Galvo::_parseNextPoint(char **s, Point current, bool is_relative)
{
    float x = _parseNextFloat(s);
    float y = _parseNextFloat(s);
    if (is_relative)
    {
        return current + Dist(x, y);
    }
    else
    {
        return Point(x, y);
    }
}

/**
 * @brief Calculates a single point on a quadratic Bézier curve.
 */
Point XY2Galvo::_pointOnQuadraticBezier(Point p0, Point p1, Point p2, float t)
{
    float omt = 1.0f - t;
    float omt2 = omt * omt;
    float t2 = t * t;

    // Convert Points to Dists (vectors from origin) to perform vector math
    Dist v0(p0.x, p0.y);
    Dist v1(p1.x, p1.y);
    Dist v2(p2.x, p2.y);

    // Formula: (1-t)^2 * V0 + 2(1-t)t * V1 + t^2 * V2
    // This is now valid (Dist + Dist)
    Dist r = (v0 * omt2) + (v1 * (2.0f * omt * t)) + (v2 * t2);

    // Convert the resulting vector back to a Point
    return Point(r.dx, r.dy);
}

/**
 * @brief Calculates a single point on a cubic Bézier curve.
 */
Point XY2Galvo::_pointOnCubicBezier(Point p0, Point p1, Point p2, Point p3, float t)
{
    float omt = 1.0f - t;
    float omt2 = omt * omt;
    float omt3 = omt2 * omt;
    float t2 = t * t;
    float t3 = t2 * t;

    // Convert Points to Dists (vectors from origin)
    Dist v0(p0.x, p0.y);
    Dist v1(p1.x, p1.y);
    Dist v2(p2.x, p2.y);
    Dist v3(p3.x, p3.y);

    // Formula: (1-t)^3 * V0 + 3(1-t)^2 * t * V1 + 3(1-t)t^2 * V2 + t^3 * V3
    // This is now valid (Dist + Dist)
    Dist r = (v0 * omt3) + (v1 * (3.0f * omt2 * t)) + (v2 * (3.0f * omt * t2)) + (v3 * t3);

    // Convert the resulting vector back to a Point
    return Point(r.dx, r.dy);
}

/**
 * @brief Tessellates a quadratic Bézier curve and sends it to the queue.
 */
void XY2Galvo::_tessellateQuadraticBezier(Point p0, Point p1, Point p2, uint steps, const LaserSet &set)
{
    if (steps < 2)
        steps = 2; // Need at least 2 segments
    if (steps > 250)
        steps = 250; // Avoid stack overflow on the Point array

    Point points[steps];
    for (uint i = 1; i <= steps; i++)
    {
        float t = (float)i / (float)steps;
        points[i - 1] = _pointOnQuadraticBezier(p0, p1, p2, t);
    }
    // We are already at p0, so use POLYLINE_NO_START
    drawPolyLine(steps, points, set, POLYLINE_NO_START);
}

/**
 * @brief Tessellates a cubic Bézier curve and sends it to the queue.
 */
void XY2Galvo::_tessellateCubicBezier(Point p0, Point p1, Point p2, Point p3, uint steps, const LaserSet &set)
{
    if (steps < 2)
        steps = 2;
    if (steps > 250)
        steps = 250; // Avoid stack overflow

    Point points[steps];
    for (uint i = 1; i <= steps; i++)
    {
        float t = (float)i / (float)steps;
        points[i - 1] = _pointOnCubicBezier(p0, p1, p2, p3, t);
    }
    // We are already at p0, so use POLYLINE_NO_START
    drawPolyLine(steps, points, set, POLYLINE_NO_START);
}

/**
 * @brief Public-facing function to start the path parser.
 */
void XY2Galvo::drawPath(cstr path_data, const LaserSet &set, uint tessellation_steps)
{
    // We need a non-const pointer to pass to the parser helpers,
    // as they advance the pointer as they read.
    char *s = const_cast<char *>(path_data);
    _drawPathParser(s, set, tessellation_steps);
}

/**
 * @brief The main SVG path parser state machine. Runs on Core 0.
 */
void XY2Galvo::_drawPathParser(char *s, const LaserSet &set, uint steps)
{
    Point current_pos(0, 0);
    Point path_start_pos(0, 0);
    Point last_control_point(0, 0);
    char command = ' ';

    while (*s)
    {
        // Skip whitespace
        while (isspace(*s))
            s++;
        if (!*s)
            break; // End of string

        // Get new command or repeat last one if a coordinate is next
        if (isalpha(*s))
        {
            command = *s++;
        }

        // Process the command
        switch (command)
        {
        case 'M': // MoveTo (Absolute)
        {
            current_pos = _parseNextPoint(&s, current_pos, false);
            path_start_pos = current_pos;
            moveTo(current_pos);
        }
        break;

        case 'm': // MoveTo (Relative)
        {
            current_pos = _parseNextPoint(&s, current_pos, true);
            path_start_pos = current_pos;
            moveTo(current_pos);
        }
        break;

        case 'L': // LineTo (Absolute)
        {
            current_pos = _parseNextPoint(&s, current_pos, false);
            drawTo(current_pos, set);
        }
        break;

        case 'l': // LineTo (Relative)
        {
            current_pos = _parseNextPoint(&s, current_pos, true);
            drawTo(current_pos, set);
        }
        break;

        case 'H': // Horizontal LineTo (Absolute)
        {
            current_pos.x = _parseNextFloat(&s);
            drawTo(current_pos, set);
        }
        break;

        case 'h': // Horizontal LineTo (Relative)
        {
            current_pos.x += _parseNextFloat(&s);
            drawTo(current_pos, set);
        }
        break;

        case 'V': // Vertical LineTo (Absolute)
        {
            current_pos.y = _parseNextFloat(&s);
            drawTo(current_pos, set);
        }
        break;

        case 'v': // Vertical LineTo (Relative)
        {
            current_pos.y += _parseNextFloat(&s);
            drawTo(current_pos, set);
        }
        break;

        case 'Z': // ClosePath
        case 'z':
        {
            if (current_pos != path_start_pos)
            {
                drawTo(path_start_pos, set);
            }
            current_pos = path_start_pos;
        }
        break;

        case 'C': // Cubic Bezier (Absolute)
        {
            Point p1 = _parseNextPoint(&s, current_pos, false);
            Point p2 = _parseNextPoint(&s, current_pos, false);
            Point p_end = _parseNextPoint(&s, current_pos, false);
            _tessellateCubicBezier(current_pos, p1, p2, p_end, steps, set);
            current_pos = p_end;
            last_control_point = p2;
        }
        break;

        case 'c': // Cubic Bezier (Relative)
        {
            Point p1 = _parseNextPoint(&s, current_pos, true);
            Point p2 = _parseNextPoint(&s, current_pos, true);
            Point p_end = _parseNextPoint(&s, current_pos, true);
            _tessellateCubicBezier(current_pos, p1, p2, p_end, steps, set);
            current_pos = p_end;
            last_control_point = p2;
        }
        break;

        case 'S': // Smooth Cubic Bezier (Absolute)
        {
            // p1 is reflection of last_control_point
            Point p1 = current_pos + (current_pos - last_control_point);
            Point p2 = _parseNextPoint(&s, current_pos, false);
            Point p_end = _parseNextPoint(&s, current_pos, false);
            _tessellateCubicBezier(current_pos, p1, p2, p_end, steps, set);
            current_pos = p_end;
            last_control_point = p2;
        }
        break;

        case 's': // Smooth Cubic Bezier (Relative)
        {
            // p1 is reflection of last_control_point
            Point p1 = current_pos + (current_pos - last_control_point);
            Point p2 = _parseNextPoint(&s, current_pos, true);
            Point p_end = _parseNextPoint(&s, current_pos, true);
            _tessellateCubicBezier(current_pos, p1, p2, p_end, steps, set);
            current_pos = p_end;
            last_control_point = p2;
        }
        break;

        case 'Q': // Quadratic Bezier (Absolute)
        {
            Point p1 = _parseNextPoint(&s, current_pos, false);
            Point p_end = _parseNextPoint(&s, current_pos, false);
            _tessellateQuadraticBezier(current_pos, p1, p_end, steps, set);
            current_pos = p_end;
            last_control_point = p1; // For T/t
        }
        break;

        case 'q': // Quadratic Bezier (Relative)
        {
            Point p1 = _parseNextPoint(&s, current_pos, true);
            Point p_end = _parseNextPoint(&s, current_pos, true);
            _tessellateQuadraticBezier(current_pos, p1, p_end, steps, set);
            current_pos = p_end;
            last_control_point = p1; // For T/t
        }
        break;

        case 'T': // Smooth Quadratic Bezier (Absolute)
        {
            // p1 is reflection of last_control_point
            Point p1 = current_pos + (current_pos - last_control_point);
            Point p_end = _parseNextPoint(&s, current_pos, false);
            _tessellateQuadraticBezier(current_pos, p1, p_end, steps, set);
            current_pos = p_end;
            last_control_point = p1;
        }
        break;
        case 't': // Smooth Quadratic Bezier (Relative)
        {
            // p1 is reflection of last_control_point
            Point p1 = current_pos + (current_pos - last_control_point);
            Point p_end = _parseNextPoint(&s, current_pos, true);
            _tessellateQuadraticBezier(current_pos, p1, p_end, steps, set);
            current_pos = p_end;
            last_control_point = p1;
        }
        break;

        case 'A': // Arc (Absolute)
        case 'a': // Arc (Relative)
        {
            // TODO: Arc implementation is very complex and not included yet.
            // For now, we'll just parse the 7 arguments to skip them.
            _parseNextFloat(&s); // rx
            _parseNextFloat(&s); // ry
            _parseNextFloat(&s); // x-axis-rotation
            _parseNextFloat(&s); // large-arc-flag
            _parseNextFloat(&s); // sweep-flag
            Point p_end = _parseNextPoint(&s, current_pos, (command == 'a'));
            // As a fallback, just draw a line to the end point.
            drawTo(p_end, set);
            current_pos = p_end;
        }
        break;

        // Default: command not recognized, stop parsing
        default:
            return;
        }

        // After a command, check if the last_control_point needs to be reset
        // (for S, s, T, t)
        if (command != 'c' && command != 'C' && command != 's' && command != 'S' &&
            command != 'q' && command != 'Q' && command != 't' && command != 'T')
        {
            last_control_point = current_pos;
        }
    }
}
