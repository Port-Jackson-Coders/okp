# Fusion 360 Scripts

These Python scripts generate parametric 3D models of the OKP sight using the Fusion 360 API.

## Files

- **parameters.py** - Central parameter definitions (edit this to change dimensions)
- **main_body.py** - Main housing with reflector, light, laser, battery cavities
- **picatinny_mount.py** - MIL-STD-1913 rail mount
- **battery_door.py** - Battery compartment door (TODO)

## Hood Styles

The `main_body.py` script supports three hood styles (set in `parameters.py`):

### 1. Minimal Hood
```python
HOOD_STYLE = "minimal"
```
- Top shade only
- 40mm forward of reflector
- Lightweight, modern look
- Best for: Low-profile builds, weight savings

### 2. Full Hood
```python
HOOD_STYLE = "full"
```
- OKP-77 style protective shroud
- Enclosed on 4 sides with open window
- Protects reflector from side glare
- Best for: Maximum protection, outdoor use

### 3. Skeleton Hood
```python
HOOD_STYLE = "skeleton"
```
- Structural ribs only (4 vertical fins)
- Lightest option
- Aggressive aesthetic
- Best for: Competition, weight-critical builds

## Usage

### Via Fusion 360 UI (Manual)

1. Open Fusion 360
2. Go to **Tools → Add-Ins → Scripts and Add-Ins**
3. Click **+** next to "My Scripts"
4. Navigate to this `fusion360/` folder
5. Select script and click **Run**

### Via MCP Server (Your Setup)

If you have the Fusion 360 MCP server running:

```python
# Execute main body generation
fusion360.execute_script("main_body.py")

# Execute Picatinny mount
fusion360.execute_script("picatinny_mount.py")
```

## Changing Parameters

Edit `parameters.py` to adjust dimensions:

```python
# Try different total lengths
TOTAL_LENGTH = 150.0  # Shorter, more compact

# Try different hood styles
HOOD_STYLE = "skeleton"  # Lightest option

# Adjust module positions
LIGHT_OFFSET_X = -18.0  # Move light further left
LASER_OFFSET_X = 18.0   # Move laser further right
```

After changing parameters, re-run the scripts to regenerate the models.

## Known Issues / TODO

1. **Reflector tilt angle** - Currently creates vertical cavity, needs 45° tilted construction plane
2. **Edge filleting** - `round_edges()` function is stubbed, needs edge selection logic
3. **Thread features** - Need to add threaded holes for adjustment screws
4. **Assembly** - Scripts create separate components, need assembly constraints
5. **Battery door** - Not yet implemented

## Export for 3D Printing

After generating the model:

1. Right-click component → **Save As STL**
2. Set units to **mm**
3. Set refinement to **High**
4. Export to `models/prototype/`

## Export for CNC

After generating the model:

1. Right-click component → **Save As STEP**
2. Export to `models/production/`
3. Import into CAM software (Fusion 360 CAM, etc.)
