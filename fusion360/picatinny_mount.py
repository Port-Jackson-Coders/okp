"""
OKP Sight - Picatinny Mount Generator
Creates MIL-STD-1913 compliant rail mount
"""

import adsk.core
import adsk.fusion
import traceback
from . import parameters as params

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = app.activeProduct
        rootComp = design.rootComponent

        # Create new component for mount
        occurrence = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        mountComp = occurrence.component
        mountComp.name = "Picatinny_Mount"

        # Create mount base
        create_mount_base(mountComp)

        # Create rail slots
        create_rail_slots(mountComp)

        # Create cross-bolt hole
        create_cross_bolt_hole(mountComp)

        ui.messageBox('Picatinny mount created!')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def create_mount_base(comp):
    """Create the base mounting plate"""
    sketches = comp.sketches
    xyPlane = comp.xYConstructionPlane
    sketch = sketches.add(xyPlane)

    # MIL-STD-1913 cross-section profile
    # Simplified for now - create rectangular base
    half_length = params.MOUNT_LENGTH / 2
    half_width = params.RAIL_SLOT_WIDTH / 2

    lines = sketch.sketchCurves.sketchLines
    rect = lines.addTwoPointRectangle(
        adsk.core.Point3D.create(-half_length, -half_width, 0),
        adsk.core.Point3D.create(half_length, half_width, 0)
    )

    # Extrude downward (mount sits below body)
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeature)
    distance = adsk.core.ValueInput.createByReal(-params.MOUNT_HEIGHT_OFFSET / 10)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)


def create_rail_slots(comp):
    """Create the T-slot grooves per MIL-STD-1913"""
    # MIL-STD-1913 specifies specific slot dimensions
    # Slots are 5.23mm wide, spaced 12.7mm apart (0.5 inch)

    num_slots = int(params.MOUNT_LENGTH / params.RAIL_SPACING)

    for i in range(num_slots):
        sketches = comp.sketches
        xyPlane = comp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Position slot
        x_pos = -params.MOUNT_LENGTH/2 + (i * params.RAIL_SPACING)
        slot_half_width = params.RAIL_GROOVE_WIDTH / 2
        slot_length = params.RAIL_SLOT_WIDTH * 0.8  # Slot doesn't go full width

        lines = sketch.sketchCurves.sketchLines
        slot = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_pos - slot_half_width, -slot_length/2, 0),
            adsk.core.Point3D.create(x_pos + slot_half_width, slot_length/2, 0)
        )

        # Cut slot
        extrudes = comp.features.extrudeFeatures
        prof = sketch.profiles.item(0)
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeature)
        distance = adsk.core.ValueInput.createByReal(3.0 / 10)  # 3mm deep
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)


def create_cross_bolt_hole(comp):
    """Create the cross-bolt clamping hole"""
    sketches = comp.sketches
    yzPlane = comp.yZConstructionPlane
    sketch = sketches.add(yzPlane)

    # Center the bolt hole
    circles = sketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(
        adsk.core.Point3D.create(0, -params.MOUNT_HEIGHT_OFFSET/2, 0),
        3.0 / 10  # M6 bolt = 6mm dia, 3mm radius (in cm)
    )

    # Cut through mount
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(0)
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeature)
    distance = adsk.core.ValueInput.createByReal(params.RAIL_SLOT_WIDTH / 10)
    extInput.setDistanceExtent(False, distance)
    extrudes.add(extInput)
