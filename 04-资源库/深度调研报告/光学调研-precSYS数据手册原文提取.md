# SCANLAB precSYS 数据手册 —— 原文提取（供核对用）

> 来源：SCANLAB precSYS 数据手册（文档标注 02/2026）
> <https://www.scanlab.de/sites/default/files/2026-03/SCANLAB-precSYS-EN.pdf>
> 本文件是 pdftotext -layout 的提取结果，**用于离线检索与引文核对**；
> 图片、示意图与排版信息在提取中丢失，**引用请以原 PDF 为准**。
> 笔记正文见 `05-光学篇/16-precSYS 五轴微加工：进动架构与镜片.md`。

---

``textprecSYS




5-axis micro processing
The precSYS micromachining sub system enables ultra-short-                 Key advantages:
pulsed laser micro processing of flexibly variable geometries, e.g.        • User-friendly creation of micro-processing operations with 3D
fabrication of positively/negatively conical or ideal cylindrical, round     visualization
or elliptical drill holes with high aspect ratios. The precSYS com-        • Flexible USP processing with defined variable angle of incidence
bines leading-edge high-end scan technology, integrated control,
                                                                           • Maximum dependability and stability for highest precision
embedded PC and user-friendly software. This enables laser micro
processing with ultimate dynamic performance and precision.                • 515 nm variant for even more precise laser processing
Its graphical user interface facilitates straightforward creation          • Speed-independent contour fidelity thanks to innovative
and testing of micro-processing jobs. precSYS's robust, innova-              control algorithms
tive construction ensures maximum dependability in industrial              • Designed for usage in industrial serial production
applications. Its compact, modular design and specially adapted            • Ethernet and EtherCAT control interfaces
hardware and software interfaces allow easy, optimal integration           • Highly integrated solution with embedded PC
into customer-specific laser machines and networked production
                                                                           • Ultra-precise pre-calibration and alignment software
environments (industry 4.0). precSYS offers observation ports for
process-monitoring and beam-monitoring add-ons.                            • Automatic fine adjustment (system monitoring)
                                                                           • Comprehensive on-site customer service
SCANLAB ensures time-efficient system alignment and precise
system operation thanks to factory default settings and calibra-
tion as well as automatic fine-adjustment.                                 Typical applications:               Typical industries:
                                                                           • Drilling                          • Automotive
                                                                           • Ablation                          • Electronics
                                                                           • Structuring                       • Textiles
                                                                           • Cutting                           • Medical technology
                                                                                                               • Precision engineering
 precSYS



System Overview (standard version with no options)                                                  Principle of Operation
                                                                                                    precSYS lets you 3D-position the focal
                                                                                                    spot onto workpieces with precise
                                                                                                    tracking of angles of incidence (AOI).
                                                                                                    You can simultaneously vary progression
                                                                                                    of focal motion, angles of incidence and
                                       3                                                            laser intensities etc.
                                                               2
                                                                                                    High-end scan technology with small
                                                                                5                   mirror rotation angles and low moving
                                 11
                                           4                                                        masses ensure highly dynamic processing
                                                               1                                    with trepanning or precession frequencies
                                                                                             6
                                                                                                    up to 650 Hz (39 000 rpm). The system
                                                                                7
                                                                                                    works without any rotary optics.
                                                                                        8
                                                                                                    Advanced digital encoders, control
                                                                                    9               algorithms and application-optimized
                                                                                                    servo control enable contour-true, speed-
Legend                                                                                  10          independent processing with maximum
1  Gas-purged 5-axis scan unit (x, y, z, incidence angles a, b)                                     precision. The system is servo-regulated for
   with purge gas monitoring                                                                        stable positioning at precession frequen-
2 Control electronics and embedded PC                                                               cies up to 650 Hz. Specially conceived
3 Ethernet, EtherCAT and industrial connector (connections for power, PLC,                          for USP precision processing, the optical
   laser and remote access) and status LEDs                                                         path is polarization-maintaining and
4 Water cooling for thermal stability (galvo axes and electronics separately                        accommodates pulse energies up to
   cooled)                                                                                          300 µJ at 1030 nm and 65 µJ at 515 nm.
5 Process monitoring interface
                                                                                                    System Design
6 Beam position measuring unit (Automatic Fine Adjustment)
7 Objective                                                                                         Active water cooling of beam-guidance
8 Protective glass drawer for fast and safe replacement                                             components (including galvo axes) and of
9 Process gas nozzle (adjustable in x, y, z)                                                        spatially separated electronics makes the
10 Variant with the beam exit extended downward available on request                                system robust against load-dependent
11 Software and graphical user interface (GUI)                                                      temperature fluctuations. Moreover,
                                                                                                    the system's innovative beam guidance
                                                                                                    provides suitability for up to 50 W lasers.
                                                                                                    A sealed, gas-purged optical beam path
                                                                                                    (overpressure) guarantees optimum
                                                                                                    cleanliness even in harsh industrial
High industrial suitability                                                                         conditions – thereby enhancing system
                                                                                                    service life and processing accuracy.

                                                                                                    Automatic Fine Adjustment
                                                                                                    precSYS‘s factory-precalibrated beam
                                                                                                    position measurement unit can be used for
                                                                                                    monitoring the system’s beam position. If
                                                                                                    the beam position exceeds the application-
                                                                                                    specific tolerance limit, then the software
                                                                                                    can be used to readjust the beam back to
Drawer for replaceable protec-   Industry-proven connectors        Mounting holes near objective    its original zero position by the system-
tive glass                       (Ethernet, EtherCAT, power,       for precise positioning of the   internal five galvo axes.
                                 PLC, laser) and status LEDs       beam exit (3-point support)
                                                                                                             precSYS



Advantages:                                    Automatic fine adjustment
• Beam position stabilization close to the
  working field minimizes deviations along
  the beam path from laser to workpiece                                         2
• Lastingly reproducible process results                                5
  without complicated effect analysis and                  1                            4
  manual readjustment                                                       3
• Beam position monitoring via
  maintenance software program                                                      Legend
• Automatic readjustment of beam                                                    1 Five galvo axes
  position and angle via the DrillControl                                           2 Beam splitter
  software (regulation via system-internal                                          3 Objective
  galvo axes)                                                                       4 Beam position measurement unit
• Supports precSYS alignment during                                                   (DrillControl software controlled)
  commissioning and servicing                                                       5 Laser beam path



Options
Beam conditioning components                   Beam conditioning unit
• For adapting the entrance beam's
  diameter and divergence, as well as
  adjusting circular polarization within
  the image field                                                                   Legend
• Alternatively as beam conditioning unit                                           1 Laser beam
  without housing and gas purging                                                   2 Beam expander
                                                                                      with positioner (x, y, angle),
Components for optical process                                          3
                                                                                      beam expansion factor 0.25 ... 4
monitoring                                                                      4
                                                                                      divergence adjustable
SCANLAB offers a precSYS-matched                           2
                                                                                    3 Polarization unit
camera objective with optional color filters                                          (l/2 and l/4 wave plate)
for an observation wavelength of 880           1                                    4 Housing with purge gas connector
nm ± 10 nm (Observation also possible at                                              and protective windows
other wavelengths) and attachments to
increase resolution. Additionally, customer-
supplied components can be installed at
the process observation port.


Further customer-specific solutions on         Components for optical process monitoring
request.

Innovation
With precSYS’s patented technology,
a stable, purely galvo-based 5-axis
micromachining subsystem for high-
precision manufacturing processes in
series production has been realized for                             1
the first time.                                                                     Legend
                                                                    2               1 Camera objective,
                                                                                      optionally with color filter
                                                                    3               2 Adapter
                                                                                    3 Beam splitter
                                                                                    4 Observation beam path



                                                                4
 precSYS



5-Axis Laser Focus Positioning Possibilities                                                                   Flexible Processing
                                                                                                               Due to precSYS's possibility to position
                                                                                                               the laser beam in 5 axis (x, y, z, a, b),
                                                                                                               it offers highest flexibility for process
                                                                                                               development.
                                                                                                               Circular, elliptical or linear trajectories
                                                                                                               can be defined in 2D or 3D (examples
                                                       process gas nozzle                                      are shown in the lower left figure). For
                                                                                                               any geometry, the incidence angle will
                                                                  α,β        angular
                                                                             orientation                       be controlled as specified during trajec-
                                                                                                               tory motion. Thus, precSYS can precisely
                                                                                                               execute trajectories suitable for drilling,
                                                                         laser focus
                                                                        z                                      cutting or ablation with defined laser beam
                                                                           y
                                                                                                               tilting.
                                                                          x 3D positioning
                                                                                                               For example, precession drilling – in
                                                                   laser beam axis                             contrast to typical trepanning and spiral
                                                                                                               drilling – allows processing with a heli-
                                                                                                               cally moved and simultaneously tilted laser
 2D and 3D laser focal motion examples                                                                         beam, e.g. to practically eliminate beam-
                                                                                                               caustic effects at entry edges. In this way,
                                                                                                               the precSYS's high precession frequencies
                                                                                                               even enable production of deep bore holes
                                                                                                               with high aspect ratios and vertical walls at
                                                                                                               one-second intervals.
                                                                                                               A similar effect can also be exploited when
                                                                                                               structuring or cutting walls with vertical or
                                                                                                               negative-tapered defined profiles.
        y                                z
                                                                                                               High-precision processing is possible with
                                    y                                                                          the full +/-  7.5° range of incidence angles
                x                                  x
                                                                                                               in circular image fields up to 2.5 mm in
 Angle of incidence (AOI) during laser focal motion                                                            diameter. Typically employed pulse lengths
                                                                                                               are in the USP range of 250 fs – 25 ps. In
                                                                                                               addition, markings can be created within
                                                                optical
                                                                  axis                 Laser focus             an image field of up to 5 mm in diameter.


            AOI > 0°                    AOI = 0°                   AOI < 0°        laser beam axis




            Ablation, Structuring                                          Drilling                                                Cutting



e.g.                                                                                    e.g.
       Trepanning            Spiral drilling           Precession drilling
                                                                  α                                        α                                α
                                                                                            Trepanning                           Inclined
                                                                                           with inclined                      laser beam
                                                                                            laser beam

                                                                                                                Workpiece                       Workpiece
                                                                                                                movement                        movement
                                                                                                                xy                              xy



                                                                                           Cutting kerf                     Cutting kerf
                                                                                                                                                precSYS



DrillControl software                          System integration and control
An intuitive graphical user interface (GUI)
with 3D job visualization helps you easily
create and simulate processing jobs. Com-        Control

munication between DrillControl or system        System control          Ethernet             Ethernet
                                                     (PLC) *             network              interface
control and DrillServer occurs over Ethernet                                                                             DrillServer
with TCP/IP or via the EtherCAT interface.                                                                               Embedded PC
Factory calibration enables description of        DrillControl
                                                                                        Power/PLC/Laser                  RTC6
                                                  software
laser motion directly in metric units within                                                   interface                 control boards
precSYS's cartesian image field coordinate
system.
The software depicts processing steps in
3D and enables straightforward job pro-
                                                                    Laser and             Beam
gramming, as well as varying the diverse                            other system          conditioning *
                                                                    components *
process parameters.
                                               * Certain system components (e.g. lasers, electrically-switchable gas valves, motorized polarization plates,
Job designer                                     motorized beam expanders) are typically not provided by SCANLAB.

• Definition of process sequences with
  visualization of the 3D laser path
• Management of process jobs on the
                                               DrillControl graphical user interface
  precSYS system (embedded PC)
• Comprehensive simulation and testing
  possibilities
• Parameter relationships displayed as lists
  and diagrams
• No job size limitation
• Control of up to 10 digital and 2 analog
  outputs with freely definable ramps for
  setting additional parameters (e.g. laser
  power or process gas pressure)
• Diagnostics panel (galvo status, galvo
  temperature, etc.)
• Software-based adjustments
  - aligning the focal plane to the
    precession plane
  - global offsets, scalings and rotations
    for the laser focus path
  - characteristic curves for adjusting the
    laser power control parameters
                                               3D visualisation of the laser focal motion
Functionality for Production
• Additional user interface for production
  operation
• Easy management of one or several
  systems via one software
• Remote control via Ethernet or
  EtherCAT for integration in system
  control (PLC): Simple protocol for de-       Screw geometry        Ellipse with marking Linear inner cone,       Geometric flexibi-     Lines with variable
  fining, selecting and running jobs (job      with negative cone                         interpolated outer       lity via overlapping   z positions and
                                                                                          cone                     ellipses and circles   AOI ≠ 0°
  definition via XML including validation)                                                                         (modular approach)
  and for parameter adaption for
  compensating workpiece tolerances
  (e.g. offsets)
precSYS




          1   Flexible geometries in 300-µm-thick steel    Processing Results
              (SEM image, exit side)                       precSYS 5-axis material processing enables
                                                           machining of fine geometries in the sub-
                                                           millimeter range with high aspect ratios
                                                           and quick process times, using ultra short
                                                           pulsed laser beams. Typical micro applica-
                                                           tions are ablation, structuring, drilling and
                                                           cutting.
1 mm                                                       precSYS's high-end scan technology and
                                                           innovative calibration facilitate dynamic,
                                                           highly-precise traversal of defined paths
          2   Ideally-formed round single bore hole with
                                                           throughout the entire 2.5 mm circular
              200 µm diameter from figure 1 magnified
                                                           working field. Fabrication is also possible
              (SEM image)
                                                           outside the optical axis. Thus, no XY trans-
                                                           lation stage is needed for workpiece posi-
                                                           tioning while processing bore-hole arrays in
                                                           the image field. You can assign individual
                                                           jobs to each specific bore hole, i.e. for pro-
                                                           cessing with individual parameter settings.
100 µm
                                                           Helical processing with defined laser beam
                                                           tilting allows fabrication of high quality
          3   Cross section of a 100-µm bore hole in       bore-hole entries and exits that are clean-
              200-µm thick steel with perpendicular wall   cut, burr-free and molten-free. This enables
              contour (zero taper), process time 1 s       creation of – for example – precise positive-
                                                           ly conical (V-shaped) and negatively conical
                                                           (L-shaped) or ideally cylindrical (II-shaped)
                                                           bore wall contours with high aspect ratios.
                                                           precSYS lets you execute not only
                                                           3D geometries, but also 2D marking. In
 100 µm                                                    addition to processing of circular, elliptical
                                                           or linear laser motion paths, you can also
                                                           easily mark text with various fonts and font
          4   Detail of figure 1: Elliptical bore hole,
                                                           sizes in a 5 mm circular working field (e.g.
              190 µm long, 110 µm wide (SEM image)
                                                           for labeling during process development).
                                                           In addition, more complex geometries
                                                           such as ellipses or squares with perpen-
                                                           dicular edge contours can be fabricated.
                                                           For example, figure 7 shows a 4 x 4 square
                                                           array in ceramic with 30-µm side lengths
                                                           and a 1:10 aspect ratio. Thanks to factory
100 µm
                                                           pre-calibration, the squares are precisely
                                                           positioned within the image field to main-
                                                           tain a defined 10-µm wall thickness across
          5   Detail of figure 1: Geometric flexibility
              achieved by two overlapping ellipses         the entire array.
              190 µm long and 110 µm wide, each            When the required geometry exceeds the
              (SEM image)                                  image field of 2.5 mm in diameter, supple-
                                                           mentary external axes can be employed
                                                           below the precSYS for workpiece guid-
                                                           ance. Figure 9 shows a cutting application
                                                           where segments with vertically-contoured
100 µm                                                     walls were cut out of a 200-µm-thick brass
                                                                                                      precSYS




component. The wall quality is character-       200-µm bore holes in steel – compared to a       6
ized by homogenous, defect-free surfaces        human hair, fabricated with fixed workpiece
with sharp edges.                               position, without an XY translation stage
                                                (SEM image)
Quality
The high quality, dependability and indus-
trial suitability of SCANLAB's scan solutions
are the result of long-standing experi-
ence in developing and manufacturing                                                                     500 µm
galvanometer scanners and scan systems.
SCANLAB scan heads have been deployed
by industry in large quantities for many        Detail of a 4 x 4 square hole array              7
years. Each individual scan head earns ap-      in ceramic

proval for customer delivery only after first   - Square geometry: 30 µm x 30 µm
                                                - Depth: 300 µm, Aspect ratio: 1:10
passing the SCANcheck endurance test.
                                                - Perpendicular wall contour
                                                - Corner-rounding radius: < 4 µm
Customer Service
                                                - Wall thickness: 10 µm
This highly integrated system features a        (SEM image)
product-specific customer service:
• Local support for precSYS                                                                               10 µm
  commissioning by an experienced
  service technician
                                                200-µm bore holes in 300-µm thick steel          8
• On-site maintenance and repairs
                                                (entrance side), fabricated via workpiece
• Comprehensive training for efficient          positioning with an XY translation stage
  usage of software and performance of          (SEM image)
  maintenance work
• Installation of software updates
• Remote servicing and error diagnostics
  (remote interface)
                                                                                                          1 mm
• Technical support via phone service

                                                Cutting application with perpendicular cutting   9
                                                edge contour in 200-µm thick brass
                                                (SEM image)




                                                                                                         500 µm



                                                Marking pattern for labeling                     10
                                                - Characters: 0.5 mm font size,
                                                  SimpleStraight3 font
                                                - Circle diameters: 0 mm, 0.1 mm, 0.5 mm,
                                                  1.0 mm, 1.5 mm, 2.0 mm, 2.5 mm




                                                                                                          500 µm
       precSYS

      Specifications
      Wavelength                                                                                         1030 nm                                     515 nm (Standard)               515 nm (min. focus diameter)
      Clear aperture at entrance                                                                         4 mm                                        4 mm                            4 mm
      Typical entrance beam diameter (1/e2)                                                              2 mm                                        2 mm                            2.5 mm
      Typical focus diameter in image field (1/e2) for M² = 1.2                                          20 µm                                       10.2 µm *                       8.2 µm *
      Minimum focus diameter in image field (1/e2) for M² = 1.2                                          15 µm                                       8.2 µm *                        tbd
      Typical convergence angle of focused beam (full opening angle at 1/e2 level)                       0.08 rad                                    0.08 rad                        0.1 rad
      Maximum angle of incidence (AOI)                                                                   ± 7.5°                                      ± 7.5° *                        ± 7.0° *
      Trepanning / precession frequency (for max. AOI and Ø 100 µm)                                      ≤ 650 Hz (39 000 rpm)                       ≤ 650 Hz (39 000 rpm)           ≤ 650 Hz (39 000 rpm)
      Typical pulse energy                                                                               ≤ 300 µJ                                    ≤ 65 µJ                         ≤ 100 µJ
      Typical average power                                                                              ≤ 50 W                                      ≤ 50 W                          ≤ 50 W
      Typical pulse length                                                                               250 fs – 25 ps (up to cw)                   250 fs – 25 ps (up to cw)       250 fs – 25 ps (up to cw)
      Objective focal length                                                                             75 mm                                       75 mm                           75 mm
      Effective focal length                                                                             25 mm                                       25 mm                           25 mm
      Working field size (diameter, depending on nozzle opening)
      - Precession processing                                                                            ≤ 2.5 mm                                    ≤ 2.5 mm                        ≤ 1.5 mm
      - Marking                                                                                          ≤ 5 mm                                      ≤ 5 mm                          ≤ 5 mm
      Maximum focus range in z direction                                                                 ± 1.0 mm                                    ± 1.0 mm                        ± 1.0 mm
      Maximum focus speed in z direction                                                                 10 mm/s                                     10 mm/s                         10 mm/s
      Theoretical position resolution in xy image field                                                  17 nm                                       < 20 nm                         < 20 nm
      Repeatability in image field **                                                                    ≤ 0.5 µm                         ≤ 0.5 μm                      ≤ 0.5 μm
      Theoretical resolution of incidence angle                                                          2 µrad                           2 µrad                        2 µrad
      Focus polarization (after beam conditioning)                                                       circular                         circular                      circular
      Weight                                                                                             approx. 30 kg                    approx. 30 kg                 approx. 30 kg
      Observation port wavelength                                                                        880 nm ± 10 nm;                  820 nm - 890 nm;              820 nm - 890 nm;
                                                                                                         1200 nm - 1400 nm                1230 nm - 1370 nm             1230 nm - 1370 nm
      Axes                                                                                               5 factory calibrated axes (x, y, z coordinates and 2 incidence angles a, b)
      Power supply requirements                                                                          30 V – 33 V, max. 6 A
      Data and control interfaces                                                                        Ethernet (DrillControl, remote interface for PLC/machine control, XML job definitions),
                                                                                                         EtherCAT, external job start/stop trigger
      Control of Peripherals                                                                             2-bit digital output
      (e.g. laser power or process gas pressure)*                                                        8-bit digital output (PLC)
                                                                                                         Two 12-bit analog outputs (0 … 10 V) with freely definable ramp profiles
                                                                                                         Job Busy output
      Cooling                                                                                            water, 25 °C
      Purge gas (for optical beam path)                                                                  synthetic air according to ISO 8573-1:2010, class [1:2:1] (other gas types on request)
      Process gas                                                                                        freely selectable, max. 6 bar, 1 mm process gas nozzle opening ***
      Replaceable protective glass (for fast-replacement drawer)                                         yes
      Software                                                                                           DrillControl (graphical user interface), DrillServer (on embedded PC)
      * Certain system components (e.g. lasers, electrically-switchable gas valves, motorized polarization plates, motorized beam expanders) are typically not provided by SCANLAB.
      ** Deviation of diameter and roundness over 6 hours operation load (for AOI = -7.5° ... 7.5°; Ø 0.09 mm ... 0.3 mm; f = 50 Hz ... 650 Hz; z = -1 mm ... +1 mm)
      *** Other nozzle openings are optionally available if needed.         * valid for lasers with a spectral bandwidth < 1.5 nm




      Side view precSYS                                                                                                                               Beam Entrance Side

                                            132                                                                209
                                                    76                   263.5                      96
                                                                                                                                 55




                                                                                                                                                                                                                          Product photos and figures are non-binding and may show customized features.
                                                                                                              process-
                                                                                                              monitoring
                                                                                                              components*
                                                                                                                                 271




                                                                                                                                                                                                                     p
                                                                                                                                                                                                                 dee
                                                                                                                                                                                                              -9
                                                                                                                                                                                                        x M4      d eep
                                                                                                                                                                                                                          02 / 2026 Information is subject to change without notice.




                            300                                                                                                                                                     50                4        -6
                                                                                                                                                                                                            H7
                                                                                                                                                                                                         Ø4
                                                                                                                                                                                                     2x
                                                                                                                                                9.9±0.5
                                                                                                                               130




                                                                                                                                                                                                     19 31
104




                                                                         3x Ø10+0.010/+0.019
                                                                                                                                               3±0.3




                                                                              2x Ø6.65
                                                                                                                                                                                                             49.4
                                                                                                                             1




             beam conditioning unit *
                                                     4,4




                                                                                                                                                                                                     beam entrance
                                                           111.08                   200                        164                                                          100.03          92
                                                                                                                                     55.7 +1/-1.4




                                           * optional                                                                                                                            303.5                 4
                                                                                           90**




                                           ** variant with the beam exit extended                                                                                 Ø80 h6
                                              downward available on request                                                                                       Ø90 h6                 beam exit
                                           (all dimensions in mm)




      SCANLAB GmbH · Siemensstr. 2a · 82178 Puchheim · Germany                    SCANLAB America, Inc. · 100 Illinois St · St. Charles, IL 60174 · USA
      Tel. +49 89 800 746-0 · info@scanlab.de · www.scanlab.de                    Tel. +1 630 797-2044 · info@scanlab-america.com · www.scanlab-america.com

``