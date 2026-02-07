import adsk.core, adsk.fusion
import traceback

def run(context):
    """Safe OKP sight variant generator"""
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

        print("Starting OKP sight generation...")
        print("=" * 60)

        # Create variants
        results = []
        results.append(("Minimal", create_minimal_variant(root, -25.0)))
        results.append(("Full", create_full_variant(root, 0)))
        results.append(("Skeleton", create_skeleton_variant(root, 25.0)))

        # Print results
        success_count = sum(1 for _, success in results if success)

        for name, success in results:
            status = "✓" if success else "✗"
            print(f"{status} {name} variant")

        print("=" * 60)
        print(f"Created {success_count}/3 variants")
        print("")
        print("LEFT:   MINIMAL - Top shade only")
        print("CENTER: FULL - Protective shroud (4 walls)")
        print("RIGHT:  SKELETON - 4 vertical ribs")

        return True

    except Exception as e:
        print(f"FATAL: {str(e)}")
        print(traceback.format_exc())
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
        print(f"Minimal error: {str(e)}")
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
        print(f"Full error: {str(e)}")
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

        # 4 ribs
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
        print(f"Skeleton error: {str(e)}")
        return False


run({})
