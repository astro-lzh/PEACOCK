# Examples

Explore how different transitions record absorption, scattering and re-emission in
galactic winds.

(first-spectrum)=
## Start with a C II simulation

The [getting-started tutorial](getting-started.md) runs a complete synthetic C II model
and plots its escaping spectrum. It uses one configuration and one clump catalogue for
CPU and GPU runs. The example has a flat continuum source and 50 pc clumps with both
random cloud motion and radial outflow. Clump centers lie beyond
100 pc, and each complete clump fits inside the 950 pc outer boundary.

```{figure} assets/research/cii-100k-v150-spectrum.png
:alt: Continuum-normalized C II spectrum from the shared quick-start model, plotted against redward-positive velocity relative to C II 1334.53 angstroms.
:width: 100%

The C II tutorial uses 100,000 continuum photons and a 150 km s⁻¹ radial outflow. Flux is measured relative to the incident continuum, shown at one.
```

Use the [example model settings](#configurations) below to inspect the physical inputs.
The [output guide](outputs.md) explains velocity bins, aperture selection and the saved
data table.

{download}`Download the plotted spectrum (CSV) <assets/research/cii-100k-v150-spectrum.csv>`

(spectra)=
## Example spectra

Black shows the measured spectrum, gray bars show its $1\sigma$ uncertainties and red
shows the fitted profile. These observed fits illustrate research applications of
PEACOCK. The {ref}`distributed line catalog <lines>` lists the selections available
to run with the current source download; the Si III and Si IV research examples below
have no bundled command-line selector.

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

(cii-fit)=
## C II fit and DNN check in J1253−0312

The DNN fit follows the observed absorption trough and red emission peak. Two independent
radiative transfer runs at the same fitted parameters check the DNN prediction.

```{figure} assets/research/cii-j1253-dnn-fit.png
:alt: C II in CLASSY galaxy J1253−0312. Black points are observations, red is the DNN fit, and dashed blue is direct radiative transfer. The lower panel shows the difference between the models.
:width: 100%

The lower panel shows direct radiative transfer minus the DNN prediction, in units of the observational uncertainty $\sigma_{\mathrm{obs}}$. Its error bars show Monte Carlo uncertainty from the direct simulations.
```

(dnn-tutorial)=
## A DNN fit to C II in J1253−0312

Follow a real ultraviolet spectrum from escaping photon packets to a binned spectrum, a
neural-network prediction and two independent radiative transfer checks.

Start with the [synthetic C II tutorial](getting-started.md) if this is your first PEACOCK
calculation. The walkthrough here adds the aperture, observed pixel grid and surrogate
used for a particular galaxy fit.

- {download}`Python walkthrough <assets/research/cii-dnn-example.py>`
- {download}`J1253 C II example data <assets/research/cii-dnn-fit-data.npz>`

### 1. Choose the physical parameters

The J1253−0312 example fits three quantities. $A$ sets the clump encounter rate
at one kiloparsec, $q$ sets its radial slope, and $\log_{10} N_1$ sets the C II
column through one clump radius in the reference lower level. The wind velocity law, dust,
level-population ratio, aperture, velocity shift and continuum scale are fixed.

The model uses a $1$–$10\,\mathrm{kpc}$ halo and $50\,\mathrm{pc}$ clumps. The training
set samples $A$ from $1$ to $9\,\mathrm{kpc}^{-1}$ uniformly in its logarithm,
$q$ from $1$ to $3$, and $\log_{10} N_1$ from $14.3$
to $15.3$.

### 2. Bin the escaped packets

Download both files above and place them beside peacock.py in an extracted source folder.
The transport source supplies the simulator. The walkthrough uses NumPy for spectral
processing and replay.

The binning command reads the ASCII observer detuning and Doppler width, converts each
escape to velocity relative to C II $1334.53\,\text{Å}$, and selects photons inside a projected
aperture of $4.585\,\mathrm{kpc}$. It counts escapes in $232$ fine bins, normalizes the
spectrum over the fitting window and maps it onto the $50$ observed pixels by bin
overlap.

The following command uses the bundled synthetic C II configuration to demonstrate
binning. The observed fit uses a separate radial FCC catalogue family and
application-specific source preparation.

```bash
python3 -m pip install numpy
python3 peacock.py build --backend cpu
python3 peacock.py run --line CII1334 --nphot 20000 --output run/cii-binning
python3 cii-dnn-example.py bin cii-dnn-fit-data.npz run/cii-binning cii-binned.npz
```

### 3. Train on parameter and spectrum pairs

The J1253 training library used 2,000 physical parameter vectors and 120,000 launched
packets per simulation. Each row of the input matrix gives the three physical parameters.
The target row is the 232-bin spectrum after the same aperture selection and
normalization. The network learns the mapping from model parameters to emergent flux
density.

To construct a new library for equal-size clumps, turn the encounter rate $\kappa(r)=A(r/r_0)^{-q}$
into a number density by dividing by the clump cross section $\pi R_{\mathrm{cl}}^2$, with
$r_0=1\,\mathrm{kpc}$. Integrate the density over the halo to obtain the clump count. The supplied
FCC generator, tools/fcc_clump_geometry.py, takes that count with --n-clouds and the slope
with --volume-beta.

Use the entire position file for catalogue placement and point TLAC_CLUMP_FILE to it. In
the cloud section, set the reference lower-level C II column to $10^\ell\,\mathrm{cm}^{-2}$,
where $\ell=\log_{10}(N_1/\mathrm{cm}^{-2})$. Run and
bin one spectrum for each parameter row. Stack the fine spectra in the same row order as
the parameters and save them as theta and fine in library.npz. Recreating the archived
J1253 network requires its full training library and catalogue construction.

The training code below uses the study’s network structure and settings. TensorFlow is a
separate dependency for training. Keep independent simulations outside the training set to
check predictions where the network has not seen a simulated spectrum.

```python
import numpy as np
import tensorflow as tf

with np.load('library.npz', allow_pickle=False) as lib:
    x = lib['theta'].astype(float)  # A [kpc^-1], q, log10(N1 [cm^-2])
    y = lib['fine']                # shape: (models, 232)
x[:, 0] = np.log10(x[:, 0])
x_mean, y_mean = x.mean(axis=0), y.mean(axis=0)
x_scale, y_scale = x.std(axis=0), y.std(axis=0)
x_scale[x_scale == 0] = 1
y_scale[y_scale == 0] = 1

net = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(3,)),
    *[tf.keras.layers.Dense(n, activation='relu') for n in (128, 256, 256, 128)],
    tf.keras.layers.Dense(232),
])
net.compile(optimizer=tf.keras.optimizers.Adam(3e-4), loss='mse')
net.fit((x - x_mean) / x_scale, (y - y_mean) / y_scale,
        epochs=500, batch_size=128)
```

### 4. Fit the observed spectrum

The original fit used nested sampling with independent uniform priors in $\log_{10} A$,
$q$ and $\log_{10} N_1$. For each sampled point, the DNN predicts the fine-bin
spectrum. Apply the fixed velocity offset and continuum scale, integrate over the observed
pixels and compare with the measured flux. The fit used observational variance plus the
training library’s estimated packet variance.

For a new fit, use the same binning and normalization as the observations. Score each
trial by summing the squared data–prediction residuals divided by the corresponding
variances. Search within the parameter ranges used to train the network and save the
best-scoring point.

The replay evaluates the saved network at all 3,606 archived candidate samples and
recomputes their likelihood ranking. It selects the original maximum-likelihood sample and
writes the model and data on the same velocity grid. A fresh nested fit would generate a
new set of samples.

```bash
python3 cii-dnn-example.py replay cii-dnn-fit-data.npz --output cii-comparison.csv
```

### 5. Rerun transport at the fitted parameters

The selected point has $A=6.375\,\mathrm{kpc}^{-1}$, $q=1.685$ and $\log_{10} N_1=14.576$. Keep the cloud
geometry, source and observing settings fixed, then change the photon seeds and rerun the
full simulation. Bin both direct spectra with the same aperture, normalization, velocity
shift, pixel edges and flux scale as the DNN prediction.

The replay compares the DNN with the saved direct spectra from two independent
$120{,}000$-packet runs. At this point the root-mean-square difference is $1.01\times10^{-5}$
in the normalized flux-density units, or $1.11$ times the per-pixel Monte Carlo
uncertainty in RMS. The CSV contains both runs, their mean and the velocity-dependent
residual to the DNN.

This check measures the surrogate error at the selected point. The study also checked 16
separate points using two independent runs at each point before fitting the observations.

For a new fit, prepare two copies of its selected configuration, fit-seed-a.cfg and
fit-seed-b.cfg. Use the same complete catalogue and an explicit, identical grid random
seed in both files. Set a different run random seed in each copy, then generate and bin
both independent spectra.

```bash
python3 peacock.py run --line CII1334 --config fit-seed-a.cfg --nphot 120000 --output run/cii-check-a
python3 peacock.py run --line CII1334 --config fit-seed-b.cfg --nphot 120000 --output run/cii-check-b
python3 cii-dnn-example.py bin cii-dnn-fit-data.npz run/cii-check-a cii-check-a.npz
python3 cii-dnn-example.py bin cii-dnn-fit-data.npz run/cii-check-b cii-check-b.npz
```

(run)=
## Run a bundled example

```bash
python3 peacock.py run --line HI1216 --backend cpu --output run/lya
python3 peacock.py run --line SiII1190 --backend cuda --output run/si1190-cuda
```

The bundled configurations are synthetic. See the [build and run
guide](getting-started.md) for installation and the {ref}`line catalog <lines>` for
available profiles.

(configurations)=
## Example model settings

Use these synthetic configurations as starting points for your own runs. Open a
configuration to see the full set of inputs.

### Lyα 1216

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

### C II 1334/1335

These are the settings used by the shared quick-start configuration.

| Setting | Value |
| --- | --- |
| Continuum photons | 100,000 |
| Source spectrum | Flat continuum, $\pm600\,\mathrm{km}\,\mathrm{s}^{-1}$ |
| Clump placement | Centers beyond $100\,\mathrm{pc}$; complete clumps inside $950\,\mathrm{pc}$ |
| Clump radius | $50\,\mathrm{pc}$ |
| Filling factor | $10\%$ |
| Ion column across one clump radius | $3\times10^{15}\,\mathrm{cm}^{-2}$ |
| Clump temperature | $10^{4}\,\mathrm{K}$ |
| Clump motion | $25\,\mathrm{km}\,\mathrm{s}^{-1}$ dispersion per axis and $150\,\mathrm{km}\,\mathrm{s}^{-1}$ radial outflow |
| Level population ratio | $n_2/n_1=0.3$ |

The same complete catalogue supplies the clump positions to CPU and GPU runs.

- {download}`View the quick-start configuration <assets/examples/cii/quickstart.cfg>`
- {download}`Download its clump catalogue <assets/examples/cii/quickstart-clumps.txt>`

### Si II 1190

| Setting | Value |
| --- | --- |
| Source spectrum | Flat continuum, $\pm300\,\mathrm{km}\,\mathrm{s}^{-1}$ |
| Gas geometry | Smooth sphere, radius $1000\,\mathrm{pc}$ |
| Line optical depth | $1$ |
| Gas temperature | $10^{5}\,\mathrm{K}$ |
| Level population ratio | $n_2/n_1=0.4$ |

{download}`View the bundled configuration <assets/research/run-si-ii-1190.cfg>`

### C IV 1548/1551

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

(outputs)=
## Photon scattering statistics

Four C II models from {ref}`Li+2026a <li-2026a>` produce similar integrated spectra
even though their clumps intercept photons at different radii. In the legend,
$q_{\mathrm{enc}}$ sets how quickly the encounter rate falls with radius and $\mathcal A$ sets
its scale. Each curve combines two independent simulations of one million photon packets.

```{figure} assets/research/cii-scattering-four-panel.png
:alt: Four C II models compared by first and last scattering radii, the radial distribution of scattering events, and the fraction of scattered escape packets with at least N scatters.
:width: 100%

The top row shows the first and last scattering radii for photons that scattered and escaped. Lower left shows the fraction of recorded scattering events in each $1\,\mathrm{kpc}$ radial bin, including repeated events. Lower right shows the fraction of scattered, escaping photons with at least $N$ scatters.
```

As the encounter rate falls more steeply, scattering shifts inward and more escaped
photons undergo repeated scattering. These differences can be difficult to see in the
integrated spectrum alone.
