import adsk.core, adsk.fusion
import traceback

def run(context):
    """OKP sight variants - UPRIGHT orientation"""
    try:
        app = adsk.core.Application.get()
        design = adsk.fusion.Design.cast(app.activeProduct)

        if not design:
            print("ERROR: No active design")
            return False

        root = design.rootComponent
        print("Creating upright OKP sights...")
        print("=" * 60)

        # Create all 3 variants standing upright
        results = []
        results.append(("Minimal", create_minimal_upright(root, -25.0)))
        results.append(("Full", create_full_upright(root, 0)))
        results.append(("Skeleton", create_skeleton_upright(root, 25.0)))

        success_count = sum(1 for _, s in results if s)
        for name, success in results:
            print(f"{'✓' if success else '✗'} {name}")

        print("=" * 60)
        print(f"Created {success_count}/3 upright variants")
        print("")
        print("All sights now standing upright on their mounts")
        print("Pointing forward along +X axis")
        return True

    except Exception as e:
        print(f"FATAL: {str(e)}")
        return False


def create_minimal_upright(root, x_offset):
    """Minimal variant - standing upright"""
    try:
        extrudes = root.features.extrudeFeatures

        # Main body - sketch on XZ plane (vertical), extrude in Y
        sk = root.sketches.add(root.xZConstructionPlane)
        sk.name = "Minimal_Body"
        lines = sk.sketchCurves.sketchLines

        # Draw side profile (length x height)
        # X: -8.25 to +8.25 cm (165mm length)
        # Z: 0 to 4.5 cm (45mm height)
        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset - 8.25, 0, 0),
            adsk.core.Point3D.create(x_offset + 8.25, 4.5, 0)
        )

        # Extrude in Y direction to create width
        prof = sk.profiles.item(0)
        ext = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        # Extrude symmetrically: -2.5 to +2.5 cm (50mm width)
        ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(2.5))
        ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-2.5))

        body = extrudes.add(ext)
        body.name = "Minimal_Body"

        # Picatinny mount - below the body
        mount_sk = root.sketches.add(root.xZConstructionPlane)
        mount_sk.name = "Minimal_Mount"
        mount_lines = mount_sk.sketchCurves.sketchLines

        # Mount: 50mm long, 10mm tall, below body
        mount_rect = mount_lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset - 2.5, -1.0, 0),
            adsk.core.Point3D.create(x_offset + 2.5, 0, 0)
        )

        mount_prof = mount_sk.profiles.item(0)
        mount_ext = extrudes.createInput(mount_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        mount_ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.05))
        mount_ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-1.05))

        mount = extrudes.add(mount_ext)
        mount.name = "Minimal_Mount"

        # Minimal hood - top shade above body
        hood_sk = root.sketches.add(root.xZConstructionPlane)
        hood_sk.name = "Minimal_Hood"
        hood_lines = hood_sk.sketchCurves.sketchLines

        # Hood at front (x_offset +2 to +6), above body (z: 4.5 to 4.8)
        hood_rect = hood_lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset + 2.0, 4.5, 0),
            adsk.core.Point3D.create(x_offset + 6.0, 4.8, 0)
        )

        hood_prof = hood_sk.profiles.item(0)
        hood_ext = extrudes.createInput(hood_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        hood_ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(2.5))
        hood_ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-2.5))

        hood = extrudes.add(hood_ext)
        hood.name = "Minimal_Hood"

        return True

    except Exception as e:
        print(f"Minimal error: {str(e)}")
        return False


def create_full_upright(root, x_offset):
    """Full variant - standing upright"""
    try:
        extrudes = root.features.extrudeFeatures

        # Main body
        sk = root.sketches.add(root.xZConstructionPlane)
        sk.name = "Full_Body"
        lines = sk.sketchCurves.sketchLines

        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset - 8.25, 0, 0),
            adsk.core.Point3D.create(x_offset + 8.25, 4.5, 0)
        )

        prof = sk.profiles.item(0)
        ext = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(2.5))
        ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-2.5))
        extrudes.add(ext)

        # Mount
        mount_sk = root.sketches.add(root.xZConstructionPlane)
        mount_sk.name = "Full_Mount"
        mount_lines = mount_sk.sketchCurves.sketchLines

        mount_lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset - 2.5, -1.0, 0),
            adsk.core.Point3D.create(x_offset + 2.5, 0, 0)
        )

        mount_prof = mount_sk.profiles.item(0)
        mount_ext = extrudes.createInput(mount_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        mount_ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.05))
        mount_ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-1.05))
        extrudes.add(mount_ext)

        # Full hood - protective box (sketch outer and inner for walls)
        hood_sk = root.sketches.add(root.xZConstructionPlane)
        hood_sk.name = "Full_Hood"
        hood_lines = hood_sk.sketchCurves.sketchLines

        # Outer box
        hood_lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset + 1.0, 4.5, 0),
            adsk.core.Point3D.create(x_offset + 6.0, 8.0, 0)
        )

        # Inner window
        hood_lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset + 1.0, 4.5, 0),
            adsk.core.Point3D.create(x_offset + 6.0, 7.7, 0)
        )

        # Extrude walls only
        hood_prof = hood_sk.profiles.item(1)  # Wall profile
        hood_ext = extrudes.createInput(hood_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        hood_ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(2.25))
        hood_ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-2.25))
        extrudes.add(hood_ext)

        return True

    except Exception as e:
        print(f"Full error: {str(e)}")
        return False


def create_skeleton_upright(root, x_offset):
    """Skeleton variant - standing upright with 4 ribs"""
    try:
        extrudes = root.features.extrudeFeatures

        # Main body
        sk = root.sketches.add(root.xZConstructionPlane)
        sk.name = "Skeleton_Body"
        lines = sk.sketchCurves.sketchLines

        rect = lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset - 8.25, 0, 0),
            adsk.core.Point3D.create(x_offset + 8.25, 4.5, 0)
        )

        prof = sk.profiles.item(0)
        ext = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(2.5))
        ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-2.5))
        extrudes.add(ext)

        # Mount
        mount_sk = root.sketches.add(root.xZConstructionPlane)
        mount_sk.name = "Skeleton_Mount"
        mount_lines = mount_sk.sketchCurves.sketchLines

        mount_lines.addTwoPointRectangle(
            adsk.core.Point3D.create(x_offset - 2.5, -1.0, 0),
            adsk.core.Point3D.create(x_offset + 2.5, 0, 0)
        )

        mount_prof = mount_sk.profiles.item(0)
        mount_ext = extrudes.createInput(mount_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        mount_ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.05))
        mount_ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-1.05))
        extrudes.add(mount_ext)

        # 4 vertical ribs
        for i in range(4):
            rib_sk = root.sketches.add(root.xZConstructionPlane)
            rib_sk.name = f"Skeleton_Rib{i+1}"
            rib_lines = rib_sk.sketchCurves.sketchLines

            rib_x = (x_offset + 6.0) - (i * 1.125)

            # Rib: thin vertical element above body
            rib_lines.addTwoPointRectangle(
                adsk.core.Point3D.create(rib_x - 0.15, 4.5, 0),
                adsk.core.Point3D.create(rib_x + 0.15, 7.0, 0)
            )

            rib_prof = rib_sk.profiles.item(0)
            rib_ext = extrudes.createInput(rib_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
            rib_ext.setDistanceExtent(False, adsk.core.ValueInput.createByReal(2.5))
            rib_ext.setDistanceExtent(True, adsk.core.ValueInput.createByReal(-2.5))
            extrudes.add(rib_ext)

        return True

    except Exception as e:
        print(f"Skeleton error: {str(e)}")
        return False


run({})
