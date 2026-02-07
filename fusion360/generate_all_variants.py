import adsk.core, adsk.fusion

def run(context):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)

    if not design:
        print("Error: No active design")
        return

    root = design.rootComponent

    # Parameters (in cm)
    total_length = 16.5
    body_width = 5.0
    body_height = 4.5

    # Spacing between variants
    spacing = 25.0  # 25cm between each variant

    # ========================================================================
    # VARIANT 1: MINIMAL HOOD (Left, X = -25cm)
    # ========================================================================
    x_offset_minimal = -spacing

    # Main body
    sketch1 = root.sketches.add(root.xYConstructionPlane)
    sketch1.name = "Minimal_MainBody"
    lines1 = sketch1.sketchCurves.sketchLines
    rect1 = lines1.addTwoPointRectangle(
        adsk.core.Point3D.create(x_offset_minimal - total_length/2, -body_width/2, 0),
        adsk.core.Point3D.create(x_offset_minimal + total_length/2, body_width/2, 0)
    )

    extrudes = root.features.extrudeFeatures
    prof1 = sketch1.profiles.item(0)
    ext1 = extrudes.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext1.setDistanceExtent(False, adsk.core.ValueInput.createByReal(body_height))
    body1 = extrudes.add(ext1)
    body1.name = "Minimal_Body"

    # Minimal hood (top shade)
    hood_sketch1 = root.sketches.add(root.xYConstructionPlane)
    hood_sketch1.name = "Minimal_Hood"
    hood_lines1 = hood_sketch1.sketchCurves.sketchLines
    hood_length = 4.0
    hood_x_front = x_offset_minimal + 6.0
    hood_x_rear = hood_x_front - hood_length

    rect_hood1 = hood_lines1.addTwoPointRectangle(
        adsk.core.Point3D.create(hood_x_rear, -body_width/2, 0),
        adsk.core.Point3D.create(hood_x_front, body_width/2, 0)
    )

    hood_prof1 = hood_sketch1.profiles.item(0)
    hood_ext1 = extrudes.createInput(hood_prof1, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    start1 = adsk.core.ValueInput.createByReal(body_height)
    hood_ext1.startExtent = adsk.fusion.OffsetStartDefinition.create(start1)
    hood_ext1.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.2))
    hood1 = extrudes.add(hood_ext1)
    hood1.name = "Minimal_Hood"

    # ========================================================================
    # VARIANT 2: FULL HOOD (Center, X = 0cm)
    # ========================================================================
    x_offset_full = 0

    # Main body
    sketch2 = root.sketches.add(root.xYConstructionPlane)
    sketch2.name = "Full_MainBody"
    lines2 = sketch2.sketchCurves.sketchLines
    rect2 = lines2.addTwoPointRectangle(
        adsk.core.Point3D.create(x_offset_full - total_length/2, -body_width/2, 0),
        adsk.core.Point3D.create(x_offset_full + total_length/2, body_width/2, 0)
    )

    prof2 = sketch2.profiles.item(0)
    ext2 = extrudes.createInput(prof2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext2.setDistanceExtent(False, adsk.core.ValueInput.createByReal(body_height))
    body2 = extrudes.add(ext2)
    body2.name = "Full_Body"

    # Full hood (hollow box)
    hood_sketch2 = root.sketches.add(root.xYConstructionPlane)
    hood_sketch2.name = "Full_Hood"
    hood_lines2 = hood_sketch2.sketchCurves.sketchLines

    full_hood_length = 5.0
    full_hood_width = 4.5
    full_x_front = x_offset_full + 6.0
    full_x_rear = full_x_front - full_hood_length

    # Outer rectangle
    outer2 = hood_lines2.addTwoPointRectangle(
        adsk.core.Point3D.create(full_x_rear, -full_hood_width/2, 0),
        adsk.core.Point3D.create(full_x_front, full_hood_width/2, 0)
    )

    # Inner rectangle (window)
    window_width = 3.8
    inner2 = hood_lines2.addTwoPointRectangle(
        adsk.core.Point3D.create(full_x_rear, -window_width/2, 0),
        adsk.core.Point3D.create(full_x_front, window_width/2, 0)
    )

    # Extrude the wall (profile 1)
    hood_prof2 = hood_sketch2.profiles.item(1)
    hood_ext2 = extrudes.createInput(hood_prof2, adsk.fusion.FeatureOperations.JoinFeatureOperation)
    start2 = adsk.core.ValueInput.createByReal(body_height)
    hood_ext2.startExtent = adsk.fusion.OffsetStartDefinition.create(start2)
    hood_ext2.setDistanceExtent(False, adsk.core.ValueInput.createByReal(3.5))
    hood2 = extrudes.add(hood_ext2)
    hood2.name = "Full_Hood"

    # ========================================================================
    # VARIANT 3: SKELETON HOOD (Right, X = +25cm)
    # ========================================================================
    x_offset_skeleton = spacing

    # Main body
    sketch3 = root.sketches.add(root.xYConstructionPlane)
    sketch3.name = "Skeleton_MainBody"
    lines3 = sketch3.sketchCurves.sketchLines
    rect3 = lines3.addTwoPointRectangle(
        adsk.core.Point3D.create(x_offset_skeleton - total_length/2, -body_width/2, 0),
        adsk.core.Point3D.create(x_offset_skeleton + total_length/2, body_width/2, 0)
    )

    prof3 = sketch3.profiles.item(0)
    ext3 = extrudes.createInput(prof3, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ext3.setDistanceExtent(False, adsk.core.ValueInput.createByReal(body_height))
    body3 = extrudes.add(ext3)
    body3.name = "Skeleton_Body"

    # Skeleton ribs (4 vertical ribs)
    rib_count = 4
    rib_thickness = 0.3
    rib_height = 2.5
    rib_spacing_val = 4.5 / (rib_count - 1)
    skel_x_front = x_offset_skeleton + 6.0

    for i in range(rib_count):
        rib_sketch = root.sketches.add(root.xYConstructionPlane)
        rib_sketch.name = f"Skeleton_Rib{i+1}"
        rib_lines = rib_sketch.sketchCurves.sketchLines
        x_pos = skel_x_front - (i * rib_spacing_val)

        rib_rect = rib_lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_pos - rib_thickness/2, -body_width/2, 0),
            adsk.core.Point3D.create(x_pos + rib_thickness/2, body_width/2, 0)
        )

        rib_prof = rib_sketch.profiles.item(0)
        rib_ext = extrudes.createInput(rib_prof, adsk.fusion.FeatureOperations.JoinFeatureOperation)
        start_rib = adsk.core.ValueInput.createByReal(body_height)
        rib_ext.startExtent = adsk.fusion.OffsetStartDefinition.create(start_rib)
        rib_ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(rib_height))
        rib = extrudes.add(rib_ext)
        rib.name = f"Skeleton_Rib{i+1}"

    print("SUCCESS: Created all 3 hood variants side-by-side!")
    print("Left (-25cm):   MINIMAL - lightweight top shade")
    print("Center (0cm):   FULL - OKP-77 style protective shroud")
    print("Right (+25cm):  SKELETON - 4 vertical ribs (lightest)")
