# Configuring a PEACOCK simulation

In the [C II tutorial](getting-started.md), the clumps move outward at the same
speed throughout the halo. To see how acceleration changes the absorption trough,
run the same wind again with an outward speed that varies with radius. Use the
same clump positions, C II column density and random motions in both calculations.

## Switch from a constant outflow to a T15 wind

The constant wind assigns every clump a radial speed of 150 km/s. In the T15
wind, a clump starts with zero radial speed and accelerates when the outward
push from the galaxy exceeds the inward pull of gravity. Light from a steady,
compact source spreads over an area proportional to $r^2$, so a cloud of fixed
mass and cross section that absorbs a fixed fraction of the incident light
experiences an outward acceleration proportional to
$r^{-2}$. For a physical example of radiation pressure on dusty clouds, see
[Thompson et al. (2015), §2.4](https://doi.org/10.1093/mnras/stv246).

PEACOCK lets the outward acceleration fall as $r^{-\alpha}$ so you can explore
how far from the galaxy the driving remains effective. An isothermal halo has a
constant circular speed $v_{\rm c}$, so its inward acceleration has magnitude
$v_{\rm c}^2/r$. For $\alpha>1$, driving fades faster than gravity. A clump can
gain speed near the galaxy, reach its maximum speed where the two accelerations
balance, and slow down farther out. See [Steidel et al. (2010), Eq. 14](https://doi.org/10.1088/0004-637X/717/1/289)
for power-law driving and [Heckman et al. (2015), Eq. 4](https://doi.org/10.1088/0004-637X/809/2/147)
for the inverse-square case with isothermal gravity.

In this dust-free C II example, the wind law sets the clump velocities before
PEACOCK transports the line photons. Both winds use a random velocity dispersion
of 25 km/s along each axis. To switch winds, copy
`examples/cii/quickstart.cfg` to `cii-t15.cfg` and replace
these two lines in `[grid]`, or download the
{download}`complete T15 configuration <assets/examples/cii/cii-t15.cfg>`.

| Constant radial speed · original lines | T15 accelerating wind · replacement lines |
| --- | --- |
| `cloud_motion_modes = ((2,1))` | `cloud_motion_modes = ((2,3))` |
| `cloud_motion_params = ((25,150,0,0,0,0))` | `cloud_motion_params = ((25,80,10,1.5,100,950))` |

Read the two motion choices from left to right. The first (`2`) draws the three
random velocity components independently from a Gaussian distribution. Keeping
the grid seed and catalogue fixed gives the same clumps the same random motions.
The second choice sets their outward speed. Change it from constant (`1`) to
accelerating (`3`). In the parameter row, keep `25` for the random dispersion
and use the remaining five entries for the wind law.

| T15 entry, in file order | Example value | Meaning |
| --- | --- | --- |
| $v_0$ | 80 km/s | Velocity scale multiplying the square root below. |
| $R$ | 10 | Sets the strength of the driving. In this velocity law the outward acceleration at launch is $(\alpha-1)R$ times gravity. |
| $\alpha$ | 1.5 | Dimensionless exponent controlling how the outward acceleration declines with radius. |
| $R_{\min}$ | 100 pc | Launch radius, where the radial wind starts at zero. |
| $R_{\max}$ | 950 pc | Outer radius through which the wind law applies. |

For a clump at radius $r$, write $x=r/R_{\min}$. Within the specified interval
PEACOCK adds the following speed along the outward radial direction:

$$
v_{\rm wind}(r)=v_0\sqrt{\max\!\left(0,\;R[1-x^{1-\alpha}]-\ln x\right)}.
$$

For the example values, the outward acceleration at launch is five times
gravity. The clumps are still accelerating at the outer edge of the modeled
shell. Their radial speed reaches 120 km/s at 200 pc and 158 km/s at 500 pc.
Outside the wind interval the clump retains its random motion. Clump placement
and wind acceleration each have their own inner and outer radii. This example
uses the same boundaries for both, as in the release's `docs/cloud-model.md`.
The [wind equation in Physical model](models.md#radial-acceleration-and-outflow-speed)
gives the $\alpha=2$ case.

## Run both winds and compare the spectra

Start in the extracted [PEACOCK 1.0.3 source directory](download.md) with the CPU build
from [Getting started](getting-started.md#cpu). Save `cii-t15.cfg` alongside
`peacock.py`. In a Bash shell, run each configuration with the **same catalogue** and
give it a fresh output directory:

```bash
python3 peacock.py run --line CII1334 --backend cpu \
    --config examples/cii/quickstart.cfg --clump-file examples/cii/quickstart-clumps.txt \
    --output run/cii-constant
python3 peacock.py run --line CII1334 --backend cpu \
    --config cii-t15.cfg --clump-file examples/cii/quickstart-clumps.txt \
    --output run/cii-t15
```

Plot both runs with the full aperture, the injected continuum as the flux reference,
and 60 bins from −600 to +600 km/s. These are the plotter's defaults for this source.

```bash
python3 tools/plot_spectrum.py run/cii-constant --output run/cii-constant/spectrum.png
python3 tools/plot_spectrum.py run/cii-t15 --output run/cii-t15/spectrum.png
```

```{figure} assets/research/cii-100k-constant-vs-t15.png
:alt: Constant and accelerating radial velocities, and their C II spectra. The T15 spectrum has a shallower blue absorption minimum shifted to a more negative velocity.
:width: 100%

The accelerating wind produces a shallower absorption trough farther to the blue.
With 20 km/s bins, the minimum shifts from −150 km/s in the constant wind to
−170 km/s in the T15 wind, and its flux rises from 0.654 to 0.725 times the
incident continuum.
```

To check the inputs of a completed run, open `resolved.cfg` in its output directory.
`clumps.txt` contains the positions supplied to that run and `atomic.atom` contains
the selected atomic network. The plotted fluxes, bin edges and Monte Carlo uncertainties
are in `spectrum.csv`.

## Read the C II configuration

The {download}`original C II configuration <assets/examples/cii/quickstart.cfg>`
sets the source of the photons, the gas they travel through, and the motion of
the clumps. This is the default for `--line CII1334`. Passing `--config` selects
your own complete configuration file. The separate
{download}`clump catalogue <assets/examples/cii/quickstart-clumps.txt>` supplies
the positions in **cm**. Radii in the configuration are in **pc**.

### Photon packets and source

| Section and setting | Example value | Meaning |
| --- | --- | --- |
| `[run] nphot` | `100000` | Number of primary photon packets launched. A value passed to `--nphot` takes precedence. |
| `[run] random_seed` | `20261104` | Integer seed for photon sampling. Change it for another photon realization in the same wind. |
| `[run] filename_prefix` | `<0>` | The launcher supplies a file prefix inside the directory you select with `--output`. |
| `[emission] position_mode`, `position_param` | `3`, `0.001` | Draw the emission radius from an exponential distribution with a scale of 0.001 pc about the halo center. This gives a compact source. |
| `[emission] p_cloud` | `0` | Fraction of packets launched inside clumps. Here all packets start outside the clumps. |
| `[emission] frequency_mode`, `frequency_param` | `3`, `600` | Inject a flat continuum over velocity offsets from −600 to +600 km/s around the reference transition. The parameter specifies the half-width. |
| `[emission] cii_ratio_21` | `0.1` | C II lower-level population ratio $n_2/n_1$. This example has one ion in the excited fine-structure level for every ten in the ground level. |

### The halo and the interior of each clump

`[grid]` describes the halo. `[cloud1]` describes the material and grid *inside*
one clump. Radii in these two configuration sections are in pc.

| Setting | `[grid]` example | `[cloud1]` example | Meaning |
| --- | --- | --- | --- |
| `type`, `size` | `2`, `1000` | `2`, `50` | Spherical grids with outer radii of 1,000 pc for the halo and 50 pc for each clump. |
| `ncells` | `(1,1,1)` | `(1,1,1)` | One cell in each spherical coordinate (radius, polar angle and azimuth). The halo cell contains the individual clumps. |
| `filling_mode`, `rmin`, `rmax` | `1`, `0`, `1000` | `1`, `0`, `50` | Fill one radial interval with the properties below. In this example the interval spans the full radius of each grid. |
| `temperature` | `10000` | `10000` | Gas temperature in K. The clump temperature sets the thermal contribution to the line width. |
| `hydrogen` | `n 0` | `c 3e15` | In this C II run, `n` supplies the reference lower-level number density in cm⁻³ and `c` supplies its radial column in cm⁻². The background density is zero. Each clump has a center-to-edge column of 3 × 10¹⁵ cm⁻², or 6 × 10¹⁵ cm⁻² through its diameter. |
| `dust` | `n 0` | `n 0` | Dust number density in cm⁻³. Both the clumps and the space between them are dust-free. |
| `velocity_mode`, `velocity_params` | `1`, `(0)` | `0`, omitted | The background has constant radial speed 0 km/s. The clump gas has zero internal bulk motion in its own frame. The motion of each whole clump is set separately below. |
| `luminosity_mode` | `1` | `1` | Selects a central source when emission is sampled from cell luminosities. The radial exponential source in this example samples positions directly, so this setting has no effect here. |
| `set_all_absorbing_dust` | omitted | `False` | With `False`, an optical-depth dust input would specify total extinction. The zero dust densities here make this switch immaterial. |

### Clump positions and velocities

The catalogue gives the clump centers. These settings determine how many centers
the simulation expects and how their clumps move. Each list has one entry per
cloud population. The example uses a single population, `cloud1`. Mode numbers
select options. They have no physical units, as with counts, seeds and flags.

| Setting in `[grid]` | Example value | Meaning |
| --- | --- | --- |
| `clouds`, `cloud_mode_schema` | `(cloud1)`, `2` | Use the population defined by the `[cloud1]` section and version 2 of the placement and motion settings. |
| `cloud_placing_modes` | `(3)` | Read the complete catalogue of clump centers. Its three Cartesian coordinates, `x y z`, are in **cm**. Pass this file with `--clump-file` when running an edited copy of the configuration. |
| `cloud_filling_factors` | `(0.1)` | Clumps occupy about 10% of the shell volume in this example. At fixed shell and clump sizes, a larger filling factor requires more clumps. |
| `cloud_rin`, `cloud_rout` | `(100)`, `(950)` | Placement bounds in pc. In the supplied catalogue, clump centers lie beyond 100 pc and each entire clump fits inside 950 pc. Changing the shell, filling factor or clump radius requires a matching catalogue. |
| `random_seed` | `31415` | Integer seed used during grid construction, including the random clump velocities. Catalogue positions come from the file. If the grid seed is omitted, the grid uses the run seed. |
| `cloud_motion_modes`, `cloud_motion_params` | `((2,1))`, `((25,150,0,0,0,0))` | Add independent Gaussian velocities with a 25 km/s dispersion in each Cartesian component to an outward radial speed of 150 km/s. These two modes use the first two parameters. |

### Output

`[output] lya = ASCII_LYA` selects the CPU text format for the main stream of
escaped photon packets. The `--line CII1334` argument selects the transitions.
CUDA stores packets in `gpu_output_*.npz`. On either backend, keep `resolved.cfg`
to see the configuration passed to transport and `atomic.atom` to identify the
atomic network.

## Use your own clump coordinates

Start with `my-clumps-pc.txt`, a plain text file with one clump center per row and
three space-separated columns, `x y z`, in parsecs relative to the halo center.
Each center must lie at or beyond the shell’s inner radius. Leave room for the
whole clump inside the outer boundary and enough space between neighbors to avoid
overlap.

If you want to practice with a known geometry, run these three lines in Python
from the PEACOCK source directory. They turn the bundled coordinates from cm into
a sample input in pc. Skip this step when using your own file.

```python
import numpy as np
bundled_cm = np.loadtxt("examples/cii/quickstart-clumps.txt")
np.savetxt("my-clumps-pc.txt", bundled_cm / 3.085677581467192e18, fmt="%.17g")
```

Save the following as `convert-clumps.py` beside `peacock.py`. The script checks
that the number of rows matches the wind configuration. It divides the shell
volume occupied by clumps by the volume of one clump and rounds to the nearest whole number.
For the bundled C II configuration, that gives **685 clumps**. For your own
wind, set the shell radii, clump radius and filling factor in the script to
match your configuration. The script also checks the boundaries and spacing
before writing the coordinates in cm.

```python
import numpy as np
from scipy.spatial import cKDTree

pc_in_cm = 3.085677581467192e18
inner_pc, outer_pc, clump_radius_pc = 100.0, 950.0, 50.0
filling_factor = 0.1
clearance = 1.000001
shell_to_clump_volume = (outer_pc**3 - inner_pc**3) / clump_radius_pc**3
expected_count = int(np.floor(filling_factor * shell_to_clump_volume + 0.5))

xyz = np.loadtxt("my-clumps-pc.txt", ndmin=2)
if xyz.shape[1] != 3 or not np.isfinite(xyz).all():
    raise ValueError("Each row must contain three finite coordinates in pc.")
if len(xyz) != expected_count:
    raise ValueError(f"Expected {expected_count} clumps, found {len(xyz)}.")

radius = np.linalg.norm(xyz, axis=1)
if radius.min() < inner_pc:
    raise ValueError("A clump center is inside the inner boundary.")
if radius.max() + clump_radius_pc * clearance > outer_pc:
    raise ValueError("A clump extends past the outer boundary or its clearance.")
distances, _ = cKDTree(xyz).query(xyz, k=2)  # first match is the clump itself
if distances[:, 1].min() <= 2 * clump_radius_pc * clearance:
    raise ValueError("Two clumps overlap or touch within the placement clearance.")

np.savetxt("my-clumps-cm.txt", xyz * pc_in_cm, fmt="%.17g")
print(f"Wrote {len(xyz)} clumps with center radii {radius.min():.2f} to {radius.max():.2f} pc.")
```

Run the conversion, then pass the resulting file to the C II model and plot the
spectrum. These commands use the constant 150 km/s wind and the 25 km/s random
dispersion from `quickstart.cfg`.

```bash
python3 convert-clumps.py
python3 peacock.py run --line CII1334 --backend cpu --config examples/cii/quickstart.cfg --clump-file my-clumps-cm.txt --output run/my-clumps
python3 tools/plot_spectrum.py run/my-clumps --output run/my-clumps/spectrum.png
```

With the practice catalogue and tutorial settings, you should recover the
original constant-wind spectrum. Open `run/my-clumps/spectrum.png` to see the
line profile or [read the spectrum in Python](outputs.md#read-a-spectrum-in-python)
from `run/my-clumps/spectrum.csv`.
