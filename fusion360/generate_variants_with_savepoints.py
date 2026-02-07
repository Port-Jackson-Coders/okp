import adsk.core, adsk.fusion
import traceback

def run(context):
    """OKP sight generator with auto-save checkpoints"""
    try:
        app = adsk.core.Application.get()
        design = adsk.fusion.Design.cast(app.activeProduct)

        if not design:
            print("ERROR: No active design")
            return False

        root = design.rootComponent
        if not root:
            print("ERROR: No root component")
            return False

        print("Starting OKP sight generation with savepoints...")
        print("=" * 60)

        # Create minimal variant
        print("\n[1/3] Creating MINIMAL variant...")
        if create_minimal_variant(root, -25.0):
            print("  ✓ Minimal variant created")
            save_checkpoint(design, "OKP_Minimal")
        else:
            print("  ✗ Minimal variant failed")

        # Create full variant
        print("\n[2/3] Creating FULL variant...")
        if create_full_variant(root, 0):
            print("  ✓ Full variant created")
            save_checkpoint(design, "OKP_Full")
        else:
            print("  ✗ Full variant failed")

        # Create skeleton variant
        print("\n[3/3] Creating SKELETON variant...")
        if create_skeleton_variant(root, 25.0):
            print("  ✓ Skeleton variant created")
            save_checkpoint(design, "OKP_Complete")
        else:
            print("  ✗ Skeleton variant failed")

        print("\n" + "=" * 60)
        print("COMPLETE! All variants created with savepoints.")
        print("")
        print("LEFT:   MINIMAL - Top shade only")
        print("CENTER: FULL - Protective shroud (4 walls)")
        print("RIGHT:  SKELETON - 4 vertical ribs")
        print("")
        print("The 4 rectangles = vertical structural ribs (like fins)")

        return True

    except Exception as e:
        print(f"FATAL: {str(e)}")
        print(traceback.format_exc())
        return False


def save_checkpoint(design, checkpoint_name):
    """Save the design at a checkpoint"""
    try:
        doc = design.parentDocument
        if doc.isSaved:
            # Save existing document
            doc.save(checkpoint_name)
            print(f"  💾 Saved checkpoint: {checkpoint_name}")
        else:
            # Document not saved yet - just mark the checkpoint
            print(f"  ✓ Checkpoint: {checkpoint_name} (not saved - use File > Save)")
        return True
    except Exception as e:
        print(f"  ⚠ Savepoint warning: {str(e)}")
        return False


def create_minimal_variant(root, x_off):
    """Minimal hood variant"""
    try:
        extrudes = root.features.extrudeFeatures

        # Main body
        sk = root.sketches.add(root.xYConstructionPlane)
        sk.name = "Minimal_Body"
        sk.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off - 8.25, -2.5, 0),
            adsk.core.Point3D.create(x_off + 8.25, 2.5, 0)
        )

        ext = extrudes.createInput(
            sk.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(4.5))
        body = extrudes.add(ext)
        body.name = "Minimal_Body"

        # Mount
        mk = root.sketches.add(root.xYConstructionPlane)
        mk.name = "Minimal_Mount"
        mk.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off - 2.5, -1.05, 0),
            adsk.core.Point3D.create(x_off + 2.5, 1.05, 0)
        )

        mext = extrudes.createInput(
            mk.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        mext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-1.0))
        mount = extrudes.add(mext)
        mount.name = "Minimal_Mount"

        # Hood (top shade)
        hk = root.sketches.add(root.xYConstructionPlane)
        hk.name = "Minimal_Hood"
        hk.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off + 2.0, -2.5, 0),
            adsk.core.Point3D.create(x_off + 6.0, 2.5, 0)
        )

        hext = extrudes.createInput(
            hk.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        start = adsk.core.ValueInput.createByReal(4.5)
        hext.startExtent = adsk.fusion.OffsetStartDefinition.create(start)
        hext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(0.3))
        hood = extrudes.add(hext)
        hood.name = "Minimal_Hood"

        return True

    except Exception as e:
        print(f"  Minimal error: {str(e)}")
        return False


def create_full_variant(root, x_off):
    """Full hood variant"""
    try:
        extrudes = root.features.extrudeFeatures

        # Main body
        sk = root.sketches.add(root.xYConstructionPlane)
        sk.name = "Full_Body"
        sk.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off - 8.25, -2.5, 0),
            adsk.core.Point3D.create(x_off + 8.25, 2.5, 0)
        )

        ext = extrudes.createInput(
            sk.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(4.5))
        extrudes.add(ext)

        # Mount
        mk = root.sketches.add(root.xYConstructionPlane)
        mk.name = "Full_Mount"
        mk.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off - 2.5, -1.05, 0),
            adsk.core.Point3D.create(x_off + 2.5, 1.05, 0)
        )

        mext = extrudes.createInput(
            mk.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        mext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-1.0))
        extrudes.add(mext)

        # Full hood (4 walls)
        hk = root.sketches.add(root.xYConstructionPlane)
        hk.name = "Full_Hood"
        lines = hk.sketchCurves.sketchLines
        # Outer
        lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off + 1.0, -2.25, 0),
            adsk.core.Point3D.create(x_off + 6.0, 2.25, 0)
        )
        # Inner
        lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off + 1.0, -1.9, 0),
            adsk.core.Point3D.create(x_off + 6.0, 1.9, 0)
        )

        hext = extrudes.createInput(
            hk.profiles.item(1),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        start = adsk.core.ValueInput.createByReal(4.5)
        hext.startExtent = adsk.fusion.OffsetStartDefinition.create(start)
        hext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(3.5))
        extrudes.add(hext)

        return True

    except Exception as e:
        print(f"  Full error: {str(e)}")
        return False


def create_skeleton_variant(root, x_off):
    """Skeleton hood variant (4 ribs)"""
    try:
        extrudes = root.features.extrudeFeatures

        # Main body
        sk = root.sketches.add(root.xYConstructionPlane)
        sk.name = "Skeleton_Body"
        sk.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off - 8.25, -2.5, 0),
            adsk.core.Point3D.create(x_off + 8.25, 2.5, 0)
        )

        ext = extrudes.createInput(
            sk.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(4.5))
        extrudes.add(ext)

        # Mount
        mk = root.sketches.add(root.xYConstructionPlane)
        mk.name = "Skeleton_Mount"
        mk.sketchCurves.sketchLines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_off - 2.5, -1.05, 0),
            adsk.core.Point3D.create(x_off + 2.5, 1.05, 0)
        )

        mext = extrudes.createInput(
            mk.profiles.item(0),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        mext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-1.0))
        extrudes.add(mext)

        # 4 ribs (structural elements)
        for i in range(4):
            rk = root.sketches.add(root.xYConstructionPlane)
            rk.name = f"Skeleton_Rib{i+1}"
            rib_x = (x_off + 6.0) - (i * 1.125)
            rk.sketchCurves.sketchLines.addTwoPointRectangle(
                adsk.core.Point3D.create(rib_x - 0.15, -2.5, 0),
                adsk.core.Point3D.create(rib_x + 0.15, 2.5, 0)
            )

            rext = extrudes.createInput(
                rk.profiles.item(0),
                adsk.fusion.FeatureOperations.NewBodyFeatureOperation
            )
            start = adsk.core.ValueInput.createByReal(4.5)
            rext.startExtent = adsk.fusion.OffsetStartDefinition.create(start)
            rext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(2.5))
            extrudes.add(rext)

        return True

    except Exception as e:
        print(f"  Skeleton error: {str(e)}")
        return False


run({})
