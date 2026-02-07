# Dimensional Specifications

## Overall Envelope

| Parameter | Value | Notes |
|-----------|-------|-------|
| Total length | 165mm | Includes battery compartment |
| Body width | 50mm | Wider than OKP-77 (42mm) for light/laser |
| Body height | 45mm | From rail to top of hood |
| Mount height | 36mm | Center of lens to rail (same as OKP-77) |

## Picatinny Mount (MIL-STD-1913)

| Parameter | Value |
|-----------|-------|
| Rail slot width | 20.6mm |
| Rail groove width | 5.23mm |
| Rail spacing | 12.7mm (0.5 inch) |
| Mount length | 50mm (4 slots) |

## Reflector Housing

| Parameter | Value | Notes |
|-----------|-------|-------|
| Reflector diameter | 30mm | For ~25mm usable aperture |
| Reflector tilt | 45° | Projects reticle forward |
| Reflector center height | 36mm | Above rail |
| LED focal distance | 112.5mm | From reflector center (half of 225mm radius) |

## Module Cavities

### Tactical Light Module
| Parameter | Value |
|-----------|-------|
| Cavity diameter | 22mm (20mm module + 2mm clearance) |
| Cavity depth | 42mm (40mm module + 2mm for lens) |
| Center position X | -15mm from centerline (left side) |
| Center position Z | 25mm above rail |

### Green Laser Module
| Parameter | Value |
|-----------|-------|
| Cavity diameter | 14mm (12mm module + 2mm clearance) |
| Cavity depth | 37mm (35mm module + 2mm for lens) |
| Center position X | +15mm from centerline (right side) |
| Center position Z | 25mm above rail |
| Angle down | 2° (for 50-yard zero) |

## Battery Compartment

| Parameter | Value | Notes |
|-----------|-------|-------|
| Battery diameter | 19mm | 18650 (18mm) + 1mm clearance |
| Battery length | 67mm | 65mm + 2mm for contacts |
| USB-C port width | 9mm | |
| USB-C port height | 3.2mm | |
| Orientation | Vertical | Rear of housing |

## Adjustment Mechanism

| Parameter | Value | Notes |
|-----------|-------|-------|
| Screw diameter | 6mm | M6 or 1/4-20 |
| Adjustment travel | ±5mm | Total 10mm range |
| Clicks per revolution | 20 | 1 MOA per click at 100 yards |
| Turret style | Recessed | vs OKP-77 exposed |

## Reticle

| Parameter | Value | Notes |
|-----------|-------|-------|
| Dot diameter | 2 MOA | At 100 yards |
| Cross arm length | 10 MOA | Each arm |
| Cross center gap | 4 MOA | Empty except for dot |
| Cross thickness | 0.5 MOA | |

## Material Allowances

### ASA 3D Print (Prototype)
- Wall thickness: 2.5-3mm minimum
- Print-in-place tolerance: 0.2-0.3mm
- Threaded inserts: M3/M4 heat-set

### CNC Aluminum (Production)
- Minimum wall thickness: 2mm (structural), 1mm (non-structural)
- Thread engagement: 1.5x diameter minimum
- Surface finish: Ra 3.2µm (as-machined), Ra 1.6µm (critical surfaces)
- Anodize build-up: +0.01mm per surface
