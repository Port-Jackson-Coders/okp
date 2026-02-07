#Author-
#Description-Simple test to verify Fusion 360 API access

import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Create a simple box
        design = app.activeProduct
        rootComp = design.rootComponent

        # Create a new sketch
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Draw a 50mm x 30mm rectangle
        lines = sketch.sketchCurves.sketchLines
        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(0, 0, 0),
            adsk.core.Point3D.create(5, 3, 0)  # 5cm x 3cm
        )

        # Extrude it 20mm
        extrudes = rootComp.features.extrudeFeatures
        prof = sketch.profiles.item(0)
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeature)
        distance = adsk.core.ValueInput.createByReal(2.0)  # 2cm
        extInput.setDistanceExtent(False, distance)
        extrudes.add(extInput)

        ui.messageBox('Success! Created a simple test box.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
