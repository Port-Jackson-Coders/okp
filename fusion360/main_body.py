"""
OKP Sight - Main Body Generator
Generates the main housing with reflector, light, laser, and battery cavities
Supports three hood styles: minimal, full, skeleton
"""

import adsk.core
import adsk.fusion
import traceback
import math
from . import parameters as params

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct

        # Get the root component
        rootComp = design.rootComponent

        # Create a new component for the main body
        occurrence = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        bodyComp = occurrence.component
        bodyComp.name = "OKP_MainBody"

        # Create main body box
        sketches = bodyComp.sketches
        xyPlane = bodyComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Draw main body rectangle (centered on origin)
        lines = sketch.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(-params.TOTAL_LENGTH/2, -params.BODY_WIDTH/2, 0),
            adsk.core.Point3D.create(params.TOTAL_LENGTH/2, params.BODY_WIDTH/2, 0)
        )

        # Extrude main body
        extrudes = bodyComp.features.extrudeFeatures
        prof = sketch.profiles.item(0)
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeature)
        distance = adsk.core.ValueInput.createByReal(params.BODY_HEIGHT / 10)  # cm
        extInput.setDistanceExtent(False, distance)
        mainBodyExtrude = extrudes.add(extInput)

        # Create battery cavity
        create_battery_cavity(bodyComp)

        # Create reflector cavity
        create_reflector_cavity(bodyComp)

        # Create light module cavity
        create_light_cavity(bodyComp)

        # Create laser module cavity
        create_laser_cavity(bodyComp)

        # Create hood based on style
        if params.HOOD_STYLE == "minimal":
            create_hood_minimal(bodyComp)
        elif params.HOOD_STYLE == "full":
            create_hood_full(bodyComp)
        elif params.HOOD_STYLE == "skeleton":
            create_hood_skeleton(bodyComp)

        # Round exterior edges
        round_edges(bodyComp)

        ui.messageBox(f'Main body created with {params.HOOD_STYLE} hood!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def create_battery_cavity(comp):
    """Create cylindrical cavity for 18650 battery (vertical orientation)"""
    sketches = comp.sketches
    yzPlane = comp.yZConstructionPlane
    sketch = sketches.add(yzPlane)

    # Position at rear of body
    x_position = -params.TOTAL_LENGTH/2 + params.BATTERY_SECTION_LENGTH/2
    y_position = 0  # Centered
    z_position = params.BODY_WALL_THICKNESS + params.BATTERY_DIAMETER/2

    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(
        adsk.core.Point3D.create(y_position, z_position, 0),
        params.BATTERY_DIAMETER/2 / 10  # cm
    )

    # Extrude cavity (cut)
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeature)
    distance = adsk.core.ValueInput.createByReal(params.BATTERY_LENGTH / 10)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)

    # USB-C port cutout (rear panel)
    create_usb_port(comp, x_position)


def create_usb_port(comp, battery_x_position):
    """Create USB-C port cutout on rear panel"""
    sketches = comp.sketches
    xyPlane = comp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    # Position on rear panel
    x = -params.TOTAL_LENGTH/2
    y = 0
    z = params.BODY_WALL_THICKNESS + params.BATTERY_DIAMETER/2

    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(
        adsk.core.Point3D.create(x - params.USB_C_WIDTH/2, y - params.USB_C_HEIGHT/2, 0),
        adsk.core.Point3D.create(x + params.USB_C_WIDTH/2, y + params.USB_C_HEIGHT/2, 0)
    )

    # Extrude cut
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeature)
    distance = adsk.core.ValueInput.createByReal(params.USB_C_DEPTH / 10)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_reflector_cavity(comp):
    """Create cylindrical cavity for parabolic reflector at 45° tilt"""
    sketches = comp.sketches

    # Create construction plane tilted 45°
    planes = comp.constructionPlanes
    planeInput = planes.createInput()
    # TODO: Create angled plane for reflector
    # This is complex - need to create offset plane and rotate

    # For now, create vertical cavity (simplification)
    yzPlane = comp.yZConstructionPlane
    sketch = sketches.add(yzPlane)

    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(
        adsk.core.Point3D.create(0, params.REFLECTOR_CENTER_HEIGHT, 0),
        params.REFLECTOR_HOUSING_DIAMETER/2 / 10
    )

    # Extrude cut
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeature)
    distance = adsk.core.ValueInput.createByReal(40 / 10)  # 40mm deep
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_light_cavity(comp):
    """Create cylindrical cavity for tactical light module (left side)"""
    sketches = comp.sketches
    yzPlane = comp.yZConstructionPlane
    sketch = sketches.add(yzPlane)

    # Position on left side
    y_position = params.LIGHT_OFFSET_X
    z_position = params.LIGHT_OFFSET_Z

    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(
        adsk.core.Point3D.create(y_position, z_position, 0),
        params.LIGHT_DIAMETER/2 / 10
    )

    # Extrude cut from front
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeature)
    distance = adsk.core.ValueInput.createByReal(params.LIGHT_DEPTH / 10)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_laser_cavity(comp):
    """Create cylindrical cavity for green laser module (right side)"""
    sketches = comp.sketches
    yzPlane = comp.yZConstructionPlane
    sketch = sketches.add(yzPlane)

    # Position on right side
    y_position = params.LASER_OFFSET_X
    z_position = params.LASER_OFFSET_Z

    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(
        adsk.core.Point3D.create(y_position, z_position, 0),
        params.LASER_DIAMETER/2 / 10
    )

    # Extrude cut from front
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeature)
    distance = adsk.core.ValueInput.createByReal(params.LASER_DEPTH / 10)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_hood_minimal(comp):
    """Create minimal hood - top shade only"""
    sketches = comp.sketches
    xyPlane = comp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    # Create top shade above reflector
    x_front = params.REFLECTOR_POSITION_X
    x_rear = x_front - params.HOOD_MINIMAL_LENGTH
    y_half = params.BODY_WIDTH/2

    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(
        adsk.core.Point3D.create(x_rear, -y_half, 0),
        adsk.core.Point3D.create(x_front, y_half, 0)
    )

    # Extrude upward from top of body
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.JoinFeature)

    # Start from top of body
    start_offset = adsk.core.ValueInput.createByReal(params.BODY_HEIGHT / 10)
    extInput.startExtent = adsk.fusion.OffsetStartDefinition.create(start_offset)

    distance = adsk.core.ValueInput.createByReal(params.HOOD_MINIMAL_THICKNESS / 10)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_hood_full(comp):
    """Create full hood - OKP-77 style protective shroud"""
    sketches = comp.sketches
    xyPlane = comp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    # Create hollow box around reflector
    x_front = params.REFLECTOR_POSITION_X + params.HOOD_FULL_LENGTH/2
    x_rear = x_front - params.HOOD_FULL_LENGTH
    y_half = params.HOOD_FULL_WIDTH/2

    # Outer rectangle
    lines = sketch.sketchCurves.sketchLines
    outer = lines.addTwoPointRectangle(
        adsk.core.Point3D.create(x_rear, -y_half, 0),
        adsk.core.Point3D.create(x_front, y_half, 0)
    )

    # Inner rectangle (window)
    window_half = params.HOOD_FULL_WINDOW_WIDTH/2
    inner = lines.addTwoPointRectangle(
        adsk.core.Point3D.create(x_rear, -window_half, 0),
        adsk.core.Point3D.create(x_front, window_half, 0)
    )

    # Extrude hollow hood
    extrudes = comp.features.extrudeFeatures
    # Select the profile between outer and inner rectangles
    for prof in sketch.profiles:
        if prof.areaProperties().area > 0:  # Select wall profile
            extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.JoinFeature)
            distance = adsk.core.ValueInput.createByReal(params.HOOD_FULL_HEIGHT / 10)
            extInput.setDistanceExtent(False, distance)
            extrudes.add(extInput)
            break


def create_hood_skeleton(comp):
    """Create skeleton hood - structural ribs only"""
    # Create multiple thin vertical ribs
    for i in range(params.HOOD_SKELETON_RIB_COUNT):
        sketches = comp.sketches
        xyPlane = comp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Space ribs evenly
        rib_spacing = params.HOOD_SKELETON_LENGTH / (params.HOOD_SKELETON_RIB_COUNT - 1)
        x_pos = params.REFLECTOR_POSITION_X - (i * rib_spacing)

        lines = sketch.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_pos - params.HOOD_SKELETON_RIB_THICKNESS/2, -params.BODY_WIDTH/2, 0),
            adsk.core.Point3D.create(x_pos + params.HOOD_SKELETON_RIB_THICKNESS/2, params.BODY_WIDTH/2, 0)
        )

        # Extrude rib upward
        extrudes = comp.features.extrudeFeatures
        prof = sketch.profiles.item(0)
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.JoinFeature)
        distance = adsk.core.ValueInput.createByReal(params.HOOD_SKELETON_RIB_HEIGHT / 10)
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def round_edges(comp):
    """Add fillets to exterior edges for modern aesthetic"""
    # Get all edges
    fillets = comp.features.filletFeatures

    # Select exterior edges (this is simplified - would need edge selection logic)
    # For now, skip - would require manual edge selection or smart filtering
    pass
