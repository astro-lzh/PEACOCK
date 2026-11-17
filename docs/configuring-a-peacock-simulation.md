# Configuring a PEACOCK simulation

The bundled C II example launches 100,000 continuum photons into a dust-free wind.
To see how the radial velocity law shapes the spectrum, run the same 685 clumps first
with a constant outward speed of 150 km/s and then with a T15 accelerating wind.
Both calculations use a C II column of $3\times10^{15}\,\mathrm{cm}^{-2}$ across one
clump radius and a random velocity dispersion of 25 km/s per Cartesian component.

## Switch from a constant outflow to a T15 wind

Copy `examples/cii/quickstart.cfg` to `cii-t15.cfg` or download the
{download}`complete T15 configuration <assets/examples/cii/cii-t15.cfg>`.
Only two lines in `[grid]` change.

| Constant radial speed · original lines | T15 accelerating wind · replacement lines |
| --- | --- |
| `cloud_motion_modes = ((2,1))` | `cloud_motion_modes = ((2,3))` |
| `cloud_motion_params = ((25,150,0,0,0,0))` | `cloud_motion_params = ((25,80,10,1.5,100,950))` |

The first mode, `2`, gives each clump three independent Gaussian velocity components.
Its parameter, `25`, is the standard deviation along each axis, in km/s. Both runs use
the same grid seed and the same cloud centers. The second mode sets the coherent outward
motion. Mode `1` adds 150 km/s at every radius. Mode `3` uses the five entries after
`25` to set a speed that varies with radius. The values below come from the wind example
in the release's `docs/cloud-model.md`.

| T15 entry, in file order | Example value | Meaning |
| --- | --- | --- |
| $v_0$ | 80 km/s | Velocity scale multiplying the square root below. |
| $R$ | 10 | Dimensionless coefficient of the outward driving term. |
| $\alpha$ | 1.5 | Dimensionless exponent controlling how the outward acceleration declines with radius. |
| $R_{\min}$ | 100 pc | Launch radius, where the radial wind starts at zero. |
| $R_{\max}$ | 950 pc | Outer radius through which the wind law applies. |

For a clump at radius $r$, write $x=r/R_{\min}$. Within the specified interval
PEACOCK adds the following speed along the outward radial direction:

$$
v_{\rm wind}(r)=v_0\sqrt{\max\!\left(0,\;R[1-x^{1-\alpha}]-\ln x\right)}.
$$

With these inputs the radial speed reaches 120 km/s at 200 pc and 158 km/s at 500 pc.
Outside the wind interval the clump retains its random motion. The placement bounds
and the wind bounds happen to coincide here. The configuration sets them separately.
The [wind equation in Physical model](models.md#radial-acceleration-and-outflow-speed)
gives the $\alpha=2$ case.

## Run both winds and compare the spectra

Start in the extracted [PEACOCK 1.0.2 source directory](download.md) with the CPU build
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

All 100,000 photons escaped in each CPU run. With 20 km/s bins, the deepest
absorption is at −150 km/s for the constant wind (flux 0.635 times the incident
continuum) and −170 km/s for the T15 wind (0.734). One T15 packet escaped outside
the plotted velocity window.
```

To check the inputs of a completed run, open `resolved.cfg` in its output directory.
`clumps.txt` contains the positions supplied to that run and `atomic.atom` contains
the selected atomic network. The plotted fluxes, bin edges and Monte Carlo uncertainties
are in `spectrum.csv`.

## Read the C II configuration

The table values come from the {download}`original C II configuration <assets/examples/cii/quickstart.cfg>`.
Use them to reproduce this example. Mode numbers, counts, seeds and flags have no
physical units. The placement and motion lists contain one entry per cloud population;
here `cloud1` is the only population.

With `--line CII1334`, omitting `--config` selects the bundled example. Passing
`--config` supplies the entire configuration for the run. Both examples above read
the same {download}`clump catalogue <assets/examples/cii/quickstart-clumps.txt>`.
It supplies positions in **cm**, while radii in the configuration are in **pc**.

### Photon packets and source

| Section and setting | Example value | Meaning |
| --- | --- | --- |
| `[run] nphot` | `100000` | Number of primary photon packets launched. A value passed to `--nphot` takes precedence. |
| `[run] random_seed` | `20261104` | Integer seed for photon sampling. Change it for another photon realization in the same wind. |
| `[run] filename_prefix` | `<0>` | The launcher supplies a file prefix inside the directory you select with `--output`. |
| `[emission] position_mode`, `position_param` | `3`, `0.001` | Draw the emission radius from an exponential distribution with a scale of 0.001 pc about the halo center. This gives a compact source. |
| `[emission] p_cloud` | `0` | Fraction of packets launched inside clumps. Here all packets start outside the clumps. |
| `[emission] frequency_mode`, `frequency_param` | `3`, `600` | Inject a flat continuum over velocity offsets from −600 to +600 km/s around the reference transition. The parameter specifies the half-width. |
| `[emission] cii_ratio_21` | `0.3` | Dimensionless C II population ratio. The excited lower fine-structure level has 0.3 times the population of the ground level. |

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

| Setting in `[grid]` | Example value | Meaning |
| --- | --- | --- |
| `clouds`, `cloud_mode_schema` | `(cloud1)`, `2` | Use the population defined by the `[cloud1]` section and version 2 of the placement and motion settings. |
| `cloud_placing_modes` | `(3)` | Read the complete catalogue of clump centers. Its three Cartesian coordinates, `x y z`, are in **cm**. Pass this file with `--clump-file` when running an edited copy of the configuration. |
| `cloud_filling_factors` | `(0.1)` | Target fraction of the shell volume occupied by clumps. With the given radii this sets a count of 685, matching the supplied catalogue. |
| `cloud_rin`, `cloud_rout` | `(100)`, `(950)` | Placement bounds in pc. In the supplied catalogue, clump centers lie beyond 100 pc and each entire clump fits inside 950 pc. Changing the shell, filling factor or clump radius requires a matching catalogue. |
| `random_seed` | `31415` | Integer seed used during grid construction, including the random clump velocities. Catalogue positions come from the file. If the grid seed is omitted, the grid uses the run seed. |
| `cloud_motion_modes`, `cloud_motion_params` | `((2,1))`, `((25,150,0,0,0,0))` | Add independent Gaussian velocities with a 25 km/s dispersion in each Cartesian component to an outward radial speed of 150 km/s. These two modes use the first two parameters. |

### Output

`[output] lya = ASCII_LYA` selects the CPU text format for the main stream of
escaped photon packets. The `--line CII1334` argument selects the transitions.
CUDA stores packets in `gpu_output_*.npz`. On either backend, keep `resolved.cfg`
to see the configuration passed to transport and `atomic.atom` to identify the
atomic network.
