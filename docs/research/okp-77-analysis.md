# OKP-77 Analysis

## What Makes the OKP-77 Work

The OKP-77 is a **collimator sight** (reflex sight) that uses a parabolic reflector to project a reticle at optical infinity. This allows the shooter to keep both eyes open and maintain situational awareness while aiming.

### Optical Principle

1. **LED at focal point** - A red LED is positioned at the focal point of a parabolic reflector
2. **Parabolic reflection** - Light from the LED reflects off the curved mirror surface
3. **Collimated beam** - Reflected light rays become parallel (collimated), appearing to come from infinity
4. **45° tilt** - The reflector is tilted 45° to project the beam forward into the shooter's line of sight
5. **Parallax-free** - Because the light is collimated, the dot appears to stay on target regardless of eye position

### Critical Dimensions

These dimensions are **driven by physics** and cannot be changed arbitrarily:

| Parameter | Value | Why |
|-----------|-------|-----|
| Reflector radius | 200-250mm | Determines focal length - larger = better collimation, harder to package |
| LED distance | 100-125mm | **Must be at focal point** = radius ÷ 2 |
| Reflector tilt | 45° | Projects beam into eye line while keeping sight compact |

### Flexible Dimensions

These can be adjusted based on design preferences:

| Parameter | OKP-77 | Our Design |
|-----------|--------|------------|
| Mount height | 36mm | 30-45mm (adjustable for preference) |
| Overall length | 95mm | 165mm (we need space for 18650 battery + light/laser) |
| Housing width | 42mm | 50mm (to fit light and laser modules) |
| Hood style | Angular steel | Swept modern style |

## OKP-77 Strengths

1. **Unlimited eye relief** - Open reflector design means no "eye box" constraint
2. **Both eyes open** - Maintains situational awareness
3. **Parallax-free** - Dot stays on target regardless of head position
4. **Fast acquisition** - Simple dot or chevron reticle
5. **Simple/rugged** - Few moving parts, proven Soviet durability

## OKP-77 Weaknesses (What We're Improving)

| OKP-77 Issue | Our Fix |
|--------------|---------|
| Chunky Soviet industrial look | Rounded edges, modern aesthetic |
| Exposed adjustment screws | Recessed turrets |
| AK dovetail mount primary | Picatinny primary, AK adapter optional |
| Painted finish | Cerakote or Type III anodize |
| Exposed battery | Integrated flush compartment with USB-C |
| Angular hood | Swept aerodynamic profile |
| No integrated light/laser | Built-in 500+ lumen light and green laser |

## Key Design Choices

### Battery: 18650 Li-ion

**Why:**
- **Capacity**: 11.1Wh (vs 0.66Wh for CR2032) = 185 hours dot-only runtime
- **Rechargeable**: USB-C charging, no disposable batteries
- **Availability**: Common, cheap, reliable
- **Voltage**: 3.7V works well with buck/boost converters for 3V LED, 5V laser, 6V light

**Trade-off:**
- Adds 65mm to length (18650 is 65mm long)
- Heavier than CR2032 (48g vs 3g)

**Verdict**: Worth it for runtime and rechargeability

### Reticle: Dot + Broken Cross

```
     |
     |
─────   ─────
     ●
─────   ─────
     |
     |
```

- **2 MOA dot** in center - precise aiming point
- **10 MOA cross arms** with **4 MOA gap** in center
- Cross helps with quick acquisition
- Gap prevents obscuring target

### Green Laser vs Red

| Feature | Green (532nm) | Red (650nm) |
|---------|---------------|-------------|
| Daylight visibility | Excellent (5-10x brighter to eye) | Poor |
| Battery life | Shorter (needs more power) | Longer |
| Cost | Higher | Lower |

**Verdict**: Green laser is worth the cost for daylight use

## References

- [OKP-7 Design (russianoptics.net)](https://russianoptics.net/OKP7.html)
- [Parabolic Reflector Theory (Thorlabs)](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=14193)
- [Red Dot Sight Physics (Wikipedia)](https://en.wikipedia.org/wiki/Red_dot_sight)
- [DIY Red Dot Sight (Instructables)](https://www.instructables.com/DIY-LED-Red-Dot-Reflex-Sight/)
