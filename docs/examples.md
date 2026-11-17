# Examples

Use the bundled models to explore how different sources and winds shape a spectrum.
The galaxy spectra below show how PEACOCK is applied to observations.

(first-spectrum)=
(start-with-a-c-ii-simulation)=
(run)=
## Run a bundled example

<span id="id4"></span>For a first run, follow the [C II tutorial](getting-started.md) and compare your output
with the {ref}`reference C II spectrum and CSV <tutorial-spectrum>`. Reuse the same backend
build to try another line. The following commands run the Lyα and Si II examples on a CPU, or the C IV
doublet on an NVIDIA GPU:

```bash
python3 peacock.py run --line HI1216 --backend cpu --output run/lya
python3 peacock.py run --line SiII1190 --backend cpu --output run/si1190
python3 peacock.py run --line CIV1548 --backend cuda --output run/civ
```

Use the [line and observable guide](choosing-a-line-and-an-observable.md) to choose
the normalization for each source.

(configurations)=
## Example model settings

<span id="id1"></span>

### Lyα from a Gaussian source

| Setting | Value |
| --- | --- |
| Source spectrum | Gaussian line, $\sigma=30\,\mathrm{km}\,\mathrm{s}^{-1}$ |
| Clump shell | $100\text{–}950\,\mathrm{pc}$ |
| Clump radius | $50\,\mathrm{pc}$ |
| Filling factor | $10\%$ |
| Radial ion column | $10^{16}\,\mathrm{cm}^{-2}$ |
| Clump temperature | $10^{4}\,\mathrm{K}$ |
| Clump motion | $25\,\mathrm{km}\,\mathrm{s}^{-1}$ dispersion per axis and $80\,\mathrm{km}\,\mathrm{s}^{-1}$ radial outflow |

{download}`View the bundled configuration <assets/research/run-lya.cfg>`

<span id="id2"></span>

### C II in a clumpy wind

For the C II continuum example, see the [full configuration, clump catalogue and wind settings](configuring-a-peacock-simulation.md).
It follows 100,000 photons through a 150 km/s outflow.

### Si II 1190

| Setting | Value |
| --- | --- |
| Source spectrum | Flat continuum, $\pm300\,\mathrm{km}\,\mathrm{s}^{-1}$ |
| Gas geometry | Smooth sphere, radius $1000\,\mathrm{pc}$ |
| Line optical depth | $1$ |
| Gas temperature | $10^{5}\,\mathrm{K}$ |
| Level population ratio | $n_2/n_1=0.4$ |

{download}`View the bundled configuration <assets/research/run-si-ii-1190.cfg>`

<span id="id3"></span>

### C IV in a clumpy wind

| Setting | Value |
| --- | --- |
| Source spectrum | Flat continuum, $\pm600\,\mathrm{km}\,\mathrm{s}^{-1}$ |
| Clump shell | $100\text{–}950\,\mathrm{pc}$ |
| Clump radius | $50\,\mathrm{pc}$ |
| Filling factor | $1\%$ |
| Radial ion column | $3\times10^{13}\,\mathrm{cm}^{-2}$ |
| Clump temperature | $10^{4}\,\mathrm{K}$ |
| Clump motion | $25\,\mathrm{km}\,\mathrm{s}^{-1}$ dispersion per axis and $80\,\mathrm{km}\,\mathrm{s}^{-1}$ radial outflow |

{download}`View the bundled configuration <assets/research/run-civ.cfg>`

(spectra)=
## Example spectra

The six panels below compare PEACOCK fits with observed galaxy spectra. Black shows
the measured flux, gray bars show its $1\sigma$ uncertainties, and red shows the fitted profile.
The [line guide](choosing-a-line-and-an-observable.md) lists the transitions available in the release.
The Si III and Si IV panels show additional research applications.

::::{container} spectrum-grid

:::{container} spectrum-card

### Si II 1190–1197

**J1428+1653**

```{figure} assets/research/example-spectrum-si-ii-1190.png
:alt: Si II 1190–1197 spectrum of J1428+1653, with observations in black and the PEACOCK fit in red.
:width: 100%

```

This group illustrates the coupled absorption and fluorescent branches near 1190–1197 Å.

:::

:::{container} spectrum-card

### Si III 1206

**J1253−0312**

```{figure} assets/research/example-spectrum-si-iii-1206.png
:alt: Si III 1206 spectrum of J1253−0312, with observations in black and the PEACOCK fit in red.
:width: 100%

```

The Si III line shows deep blueshifted absorption with extended wings and a small rise
above the continuum on the red side. This research example has no Si III selector in the
distributed transport catalog.

:::

:::{container} spectrum-card

### Lyα 1216

**J1044+0353**

```{figure} assets/research/example-spectrum-lya.png
:alt: Lyα 1216 spectrum of J1044+0353, with observations in black and the PEACOCK fit in red.
:width: 100%

```

The emission-dominated Lyα profile has a strong red peak and extended red wing. Its model
includes an intrinsic line source.

:::

:::{container} spectrum-card

### C II 1334/1335

**J1132+1411**

```{figure} assets/research/example-spectrum-cii.png
:alt: C II 1334/1335 spectrum of J1132+1411, with observations in black and the PEACOCK fit in red.
:width: 100%

```

Absorption and fluorescent re-emission constrain different branches of the coupled C II
transitions.

:::

:::{container} spectrum-card

### Si IV 1394/1403

**J1200+1343**

```{figure} assets/research/example-spectrum-siiv.png
:alt: Si IV 1394/1403 spectrum of J1200+1343, with observations in black and the PEACOCK fit in red.
:width: 100%

```

Both components show distinct absorption troughs and associated re-emission in
{ref}`Li+2026a <li-2026a>`. The current transport catalog has no Si IV selector.

:::

:::{container} spectrum-card

### C IV 1548/1551

**J1253−0312**

```{figure} assets/research/example-spectrum-civ.png
:alt: C IV 1548/1551 spectrum of J1253−0312, with observations in black and the PEACOCK fit in red.
:width: 100%

```

The doublet model follows absorption and resonant re-emission at the two component
wavelengths.

:::

::::

<span id="id5"></span><span id="cii-fit"></span><span id="c-ii-fit-and-dnn-check-in-j12530312"></span>

For **C II in J1253−0312**, see the {ref}`fit and its two direct transport checks <cii-fit>`.

<span id="dnn-tutorial"></span><span id="a-dnn-fit-to-c-ii-in-j12530312"></span>

The {ref}`spectral fitting walkthrough <dnn-tutorial>` shows how to <span id="choose-the-physical-parameters"></span>{ref}`define the wind parameters <j1253-parameters>`, <span id="bin-the-escaped-packets"></span>{ref}`bin the escaping photons <j1253-binning>`, <span id="train-on-parameter-and-spectrum-pairs"></span>{ref}`train the network <j1253-training>`, <span id="fit-the-observed-spectrum"></span>{ref}`fit the observation <j1253-fit>`, and <span id="rerun-transport-at-the-fitted-parameters"></span>{ref}`check the result with direct transport <j1253-validation>`.

(outputs)=
## Photon scattering statistics

Four C II models from {ref}`Li+2026a <li-2026a>` produce similar integrated spectra
even though their clumps intercept photons at different radii. In the legend,
$q_{\mathrm{enc}}$ sets how quickly the encounter rate falls with radius and $\mathcal A$ sets
its scale. Each curve combines two independent simulations of one million photon packets.

```{figure} assets/research/cii-scattering-four-panel.png
:name: id6
:alt: Four C II models compared by first and last scattering radii, the radial distribution of scattering events, and the fraction of scattered escape packets with at least N scatters.
:width: 100%

The top row shows the first and last scattering radii for photons that scattered and escaped. Lower left shows the fraction of recorded scattering events in each $1\,\mathrm{kpc}$ radial bin, including repeated events. Lower right shows the fraction of scattered, escaping photons with at least $N$ scatters.
```

As the encounter rate falls more steeply, scattering shifts inward and more escaped
photons undergo repeated scattering. These differences can be difficult to see in the
integrated spectrum alone.

To make these plots for your own C II run, include all escape frequencies and both
resonant and fluorescent photons. The two right-hand panels use the
[standard photon records](outputs.md#read-individual-photon-packets). The two
left-hand panels need positions recorded during scattering.

| Panel | How to calculate it |
| --- | --- |
| **Upper right · Last scattering radius** | Select escaped photons with `nscatter > 0`. CPU ASCII columns 1–3 give their last scattering position. For CUDA, use $\boldsymbol{r}_{\rm last}=\boldsymbol{r}_{\rm final}-d\,\hat{\boldsymbol n}$ to step back from the final position by the distance `dist` along the saved direction. Measure the radius from the halo center. |
| **Lower right · Number of scatterings** | Among those same photons, compute the fraction with `nscatter >= N` for each threshold $N$. A photon that scatters many times contributes once at each threshold it reaches. |
| **Upper left · First scattering radius** | Use the position where each escaped photon's scatter count first reaches one. For photons that scatter more than once, this earlier position requires a scattering history. |
| **Lower left · All scattering radii** | Use the position of each scattering event, including repeated interactions of one photon. Bin the radii in 1 kpc intervals and divide each bin count by the total number of events. |

For the probability densities in the top row, convert radii from cm to kpc and
divide each bin count by the number of scattered escapes and the bin width in kpc.

For the two left panels, record the events during transport. In a copy of the CPU
configuration, add `track_output = cii-events.dat` under `[output]`. When you run
with `--config`, this writes a new file in your working directory. Choose a fresh
filename for each run. Within each photon's history, select the rows where
`nscatter` increases by one. This skips
the intervening grid and clump crossings.
