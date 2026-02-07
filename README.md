# OKP-77 Style Reflex Sight

Modern interpretation of the OKP-77 collimator sight for Picatinny rails, designed for CNC machining and 3D printing.

## Project Goals

- **Optical Design**: Parabolic reflector red dot sight based on OKP-77 physics
- **Modernized Form**: Improved ergonomics and aesthetics over original Soviet design
- **Integrated Accessories**: Built-in tactical light and laser modules
- **Picatinny Mount**: MIL-STD-1913 compatible (vs original AK dovetail)
- **Prototyping**: ASA 3D printed models on Bambu Lab P1S
- **Production**: CNC machined aluminum (6061/7075) on future Haas Mini Mill

## Key Specifications

### Optical Parameters (Physics-Driven)
- **Reflector curvature radius**: 200-250mm (determines collimation)
- **LED focal distance**: 100-125mm (half the radius)
- **Reflector tilt**: 45° (projects reticle into eye box)
- **Eye relief**: 50-100mm+ (unlimited with open design)
- **Glass thickness**: 3-4mm (low distortion, durable)

### Design Improvements Over OKP-77
- Picatinny mount (primary) vs AK dovetail
- Integrated light and laser (vs external accessories)
- Recessed adjustment turrets (vs exposed screws)
- Modern swept hood (vs angular Soviet industrial look)
- USB-C rechargeable 18650 battery (vs disposable cells)
- Cerakote/anodized finish (vs painted)

### Reticle
- 2 MOA center dot
- Broken cross pattern (10 MOA arms with 4 MOA center gap)

### Electronics
- **Red dot LED**: 50µm red LED @ 3V, 20mA
- **Tactical light**: 500-800 lumen LED module (20-25mm dia)
- **Green laser**: <5mW 532nm (12-16mm dia)
- **Battery**: 18650 Li-ion (3.7V, 3000mAh) with USB-C charging
- **Runtime**: 185 hours (dot only), 20-30 hours (mixed use with light/laser)

## Repository Structure

```
okp/
├── README.md                 # This file
├── docs/                     # Documentation
│   ├── research/            # OKP-77 research, optics theory
│   ├── specifications/      # Detailed component specs
│   └── assembly/            # Assembly instructions
├── fusion360/               # Fusion 360 parametric scripts
│   ├── main_body.py        # Main housing generator
│   ├── picatinny_mount.py  # MIL-STD-1913 mount
│   ├── hood.py             # Protective hood/shroud
│   └── battery_door.py     # Battery compartment
├── models/                  # 3D models (STL, STEP)
│   ├── prototype/          # ASA 3D printable versions
│   └── production/         # CNC machining versions
├── electronics/            # Circuit designs, component lists
│   ├── bom.md             # Bill of materials
│   └── wiring.md          # Wiring diagrams
└── cam/                    # CAM toolpaths (future)
```

## Development Status

- [x] Research phase - OKP-77 optical design
- [x] Component sizing - Light, laser, battery modules
- [ ] Fusion 360 parametric model
- [ ] ASA prototype 3D print
- [ ] Component sourcing (PCBWay, AliExpress)
- [ ] Assembly and testing
- [ ] CNC machining version (waiting for Haas Mini Mill)

## References

- [OKP-7 Technical Details](https://russianoptics.net/OKP7.html)
- [Parabolic Reflector Optics](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=14193)
- MIL-STD-1913 Picatinny Rail Specification

## License

TBD
