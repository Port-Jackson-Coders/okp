"""
OKP Sight - Central Parameter Definitions
All dimensions in millimeters unless otherwise specified
"""

# ==============================================================================
# OPTICAL PARAMETERS (Physics-driven, do not change unless you know what you're doing)
# ==============================================================================

REFLECTOR_RADIUS = 225.0  # mm - parabolic reflector curvature radius
LED_FOCAL_DISTANCE = REFLECTOR_RADIUS / 2  # 112.5mm - LED must be at focal point
REFLECTOR_TILT_ANGLE = 45.0  # degrees - projects beam forward
REFLECTOR_DIAMETER = 30.0  # mm - usable aperture ~25mm
GLASS_THICKNESS = 3.5  # mm

# ==============================================================================
# OVERALL ENVELOPE
# ==============================================================================

TOTAL_LENGTH = 165.0  # mm
BODY_WIDTH = 50.0  # mm
BODY_HEIGHT = 45.0  # mm (from rail to top)
MOUNT_HEIGHT = 36.0  # mm (center of lens to rail)

# ==============================================================================
# PICATINNY MOUNT (MIL-STD-1913)
# ==============================================================================

RAIL_SLOT_WIDTH = 20.6  # mm
RAIL_GROOVE_WIDTH = 5.23  # mm
RAIL_SPACING = 12.7  # mm (0.5 inch)
MOUNT_LENGTH = 50.0  # mm (4 slots)
MOUNT_HEIGHT_OFFSET = 10.0  # mm below body

# ==============================================================================
# MODULE CAVITIES
# ==============================================================================

# Tactical Light Module (left side)
LIGHT_DIAMETER = 22.0  # mm (20mm module + 2mm clearance)
LIGHT_DEPTH = 42.0  # mm
LIGHT_OFFSET_X = -15.0  # mm from centerline (negative = left)
LIGHT_OFFSET_Z = 25.0  # mm above rail
LIGHT_LENS_DIAMETER = 24.0  # mm (bezel)

# Green Laser Module (right side)
LASER_DIAMETER = 14.0  # mm (12mm module + 2mm clearance)
LASER_DEPTH = 37.0  # mm
LASER_OFFSET_X = 15.0  # mm from centerline (positive = right)
LASER_OFFSET_Z = 25.0  # mm above rail
LASER_ANGLE_DOWN = 2.0  # degrees (for 50-yard zero)
LASER_LENS_DIAMETER = 16.0  # mm (bezel)

# Reflector Housing
REFLECTOR_HOUSING_DIAMETER = 32.0  # mm (30mm reflector + 2mm wall)
REFLECTOR_CENTER_HEIGHT = MOUNT_HEIGHT  # 36mm above rail
REFLECTOR_POSITION_X = 60.0  # mm from rear (front third of body)

# ==============================================================================
# BATTERY COMPARTMENT
# ==============================================================================

BATTERY_DIAMETER = 19.0  # mm (18650 = 18mm + 1mm clearance)
BATTERY_LENGTH = 67.0  # mm (65mm + 2mm for contacts)
USB_C_WIDTH = 9.0  # mm
USB_C_HEIGHT = 3.2  # mm
USB_C_DEPTH = 7.0  # mm

# ==============================================================================
# ADJUSTMENT MECHANISM
# ==============================================================================

ADJUSTMENT_SCREW_DIAMETER = 6.0  # mm (M6)
ADJUSTMENT_TRAVEL = 10.0  # mm (±5mm)
TURRET_DIAMETER = 12.0  # mm
TURRET_DEPTH = 8.0  # mm (recessed)

# ==============================================================================
# RETICLE SPECIFICATIONS
# ==============================================================================

RETICLE_DOT_MOA = 2.0  # MOA at 100 yards
RETICLE_CROSS_LENGTH_MOA = 10.0  # MOA
RETICLE_CROSS_GAP_MOA = 4.0  # MOA
RETICLE_CROSS_THICKNESS_MOA = 0.5  # MOA

# ==============================================================================
# HOOD STYLES
# ==============================================================================

HOOD_STYLE = "minimal"  # Options: "minimal", "full", "skeleton"

# Minimal hood (top shade only)
HOOD_MINIMAL_LENGTH = 40.0  # mm forward of reflector
HOOD_MINIMAL_HEIGHT = 15.0  # mm above reflector
HOOD_MINIMAL_THICKNESS = 2.0  # mm

# Full hood (OKP-77 style)
HOOD_FULL_LENGTH = 50.0  # mm forward of reflector
HOOD_FULL_WIDTH = 45.0  # mm
HOOD_FULL_HEIGHT = 35.0  # mm
HOOD_FULL_WALL_THICKNESS = 2.5  # mm
HOOD_FULL_WINDOW_WIDTH = 38.0  # mm (leaves side walls)

# Skeleton hood (structural ribs)
HOOD_SKELETON_RIB_COUNT = 4  # ribs
HOOD_SKELETON_RIB_THICKNESS = 3.0  # mm
HOOD_SKELETON_RIB_HEIGHT = 25.0  # mm
HOOD_SKELETON_LENGTH = 45.0  # mm

# ==============================================================================
# MATERIAL PROPERTIES
# ==============================================================================

# ASA 3D Print
ASA_MIN_WALL_THICKNESS = 2.5  # mm
ASA_TOLERANCE = 0.2  # mm (clearance for fit)

# CNC Aluminum
CNC_MIN_WALL_THICKNESS = 2.0  # mm (structural)
CNC_MIN_WALL_NON_STRUCTURAL = 1.0  # mm
CNC_TOLERANCE = 0.05  # mm (tight fit)
CNC_THREAD_ENGAGEMENT = 1.5  # multiplier (1.5x diameter)

# ==============================================================================
# CALCULATED VALUES (Do not edit)
# ==============================================================================

# Body sections
BATTERY_SECTION_LENGTH = BATTERY_LENGTH + 10.0  # 77mm (includes door)
REFLECTOR_SECTION_LENGTH = 50.0  # mm
FRONT_SECTION_LENGTH = TOTAL_LENGTH - BATTERY_SECTION_LENGTH - REFLECTOR_SECTION_LENGTH  # 38mm

# Wall thicknesses
BODY_WALL_THICKNESS = 3.0  # mm
BATTERY_DOOR_THICKNESS = 2.5  # mm

# Switch positions (rear panel)
MAIN_POWER_SWITCH_Z = 15.0  # mm from bottom
DOT_BRIGHTNESS_POT_Z = 25.0  # mm from bottom
LIGHT_BUTTON_Z = 35.0  # mm from bottom

# Front panel switch positions
LASER_BUTTON_X = LASER_OFFSET_X
LASER_BUTTON_Z = LASER_OFFSET_Z + 10.0  # 10mm above laser axis

print("OKP Parameters Loaded")
print(f"Total Length: {TOTAL_LENGTH}mm")
print(f"Hood Style: {HOOD_STYLE}")
print(f"LED Focal Distance: {LED_FOCAL_DISTANCE}mm")
