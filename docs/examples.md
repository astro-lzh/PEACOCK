# Examples

Use the bundled models to explore how different sources and winds shape a spectrum.
The galaxy spectra below show how PEACOCK is applied to observations.

(first-spectrum)=
(start-with-a-c-ii-simulation)=
(run)=
## Run a bundled example

<span id="id4"></span>For a first run, follow the [C II tutorial](getting-started.md) and compare your output
with the {ref}`reference C II spectrum and CSV <tutorial-spectrum>`. Once you have built
PEACOCK for your CPU or GPU, you can use the same build to try another line. These
commands run the Lyα and Si II examples on a CPU and the C IV doublet on an NVIDIA GPU.

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

The source emits Lyα with a Gaussian line profile. Scattering in the wind
redistributes those photons in frequency and reshapes the line.

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

The C II example starts with a flat continuum, so the absorption and line emission
in the spectrum arise in the wind. To reproduce the 100,000-photon run with a
150 km/s outflow, use the [C II configuration and clump catalogue](configuring-a-peacock-simulation.md).

### Si II 1190

Here a smooth sphere of gas absorbs and re-emits continuum photons through the
Si II transitions. The level population ratio sets the relative numbers of ions
in the two lower levels.

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

A flat continuum illuminates the same wind in both components of the C IV
doublet. Each component scatters with its own line strength.

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
The Si III and Si IV panels illustrate research applications beyond the lines
available in the public release. The [line guide](choosing-a-line-and-an-observable.md)
lists the transitions you can run.

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
above the continuum on the red side.

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
{ref}`Li+2026a <li-2026a>`.

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

Four winds can produce similar C II spectra even when photons scatter in different
parts of the halo. The upper panels show where photons scatter for the first and
last time. The lower panels count all scattering events by radius and show how many
scatterings a photon experiences before it escapes. The models are from {ref}`Li+2026a <li-2026a>`.

```{figure} assets/research/cii-scattering-four-panel.png
:name: id6
:alt: Four C II models compared by first and last scattering radii, the radial distribution of scattering events, and the fraction of scattered escape packets with at least N scatters.
:width: 100%

In the legend, $\mathcal A$ sets how frequently clumps intercept photons at the
reference radius, and $q_{\mathrm{enc}}$ sets how steeply that rate falls outward.
Each curve combines two independent simulations of one million photons. The first
and last radii and the scattering counts describe photons that scattered and escaped.
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
`nscatter` increases by one. This skips the intervening grid and clump crossings.
