# Spectral fitting

Which wind models can explain the C II absorption and emission in J1253−0312?
Starting from [simulated spectra](getting-started.md), this example fits the observed
line and checks the result with a fresh radiative transfer calculation.

(workflow)=
## From simulated spectra to a fit

Running a new simulation for every trial wind would make fitting slow. Instead, a
deep neural network (DNN) learns how the spectrum changes across a library of
PEACOCK simulations. The fit can then explore many winds and use direct simulations
to check the predictions that matter most.

```{figure} assets/research/figure-15-dnn.png
:alt: Five stages of the PEACOCK spectral fitting pipeline, including a DNN surrogate and direct radiative-transfer validation.
:width: 100%
:target: _static/research/figure-15-dnn.pdf

Extra simulations help where the data favor winds that are sparsely represented in the training library.
```

1. **Generate spectra with radiative transfer**

   Choose a range of winds and simulate the spectrum from each one.

2. **Train the network to predict spectra**

   Give the network each set of wind parameters together with its simulated spectrum.

3. **Fit the observed line**

   Compare the predicted absorption and emission with the data. A nested sampler estimates which combinations of wind parameters are most probable.

4. **Refine where the fit needs more models**

   If the fit favors winds near the edge of the library or in a sparsely sampled region, simulate more winds there and retrain the network.

5. **Rerun the transport at the fitted parameters**

   Check whether an independent PEACOCK simulation recovers the line shape predicted by the network.

(dnn-tutorial)=
## Fit the C II spectrum of J1253−0312

The fit recovers the galaxy’s absorption trough and red emission peak. Dashed blue
shows a direct radiative transfer calculation at the fitted parameters.

```{figure} assets/research/cii-j1253-dnn-fit.png
:name: cii-fit
:alt: C II in CLASSY galaxy J1253−0312. Black points are observations, red is the DNN fit, and dashed blue is direct radiative transfer. The lower panel shows the difference between the models.
:width: 100%

The lower panel shows direct radiative transfer minus the DNN prediction, in units of the observational uncertainty $\sigma_{\mathrm{obs}}$. Its error bars show Monte Carlo uncertainty from the direct simulations.
```

Download both files to the extracted PEACOCK source directory, beside `peacock.py`.
You can replay the published fit with NumPy, [run a new fit](#run-a-new-fit) with the
trained network, and compare the published best-fit spectrum with two saved transport
runs. To train your own network, follow step 3 with your own model library.

- {download}`Python walkthrough <assets/research/cii-dnn-example.py>`
- {download}`J1253 C II example data <assets/research/cii-dnn-fit-data.npz>`

(j1253-parameters)=
### 1. Choose the physical parameters

The fit varies how often a photon encounters clumps at one kiloparsec ($A$), how
quickly that rate falls with radius ($q$), and the C II column from the center
to the edge of one clump ($N_1$, counting ions in the reference lower level).
The [prior ranges](#run-a-new-fit) below are also the ranges used to
train the network.

For this galaxy, the clumps have a radius of $50\,\mathrm{pc}$ and occupy a shell
from $1$ to $10\,\mathrm{kpc}$. The wind velocity law, dust, lower-level population ratio and
observing aperture stay fixed, as do the velocity shift and continuum scale.

(j1253-binning)=
### 2. Bin the escaped packets

Compare the model with what the telescope collected. For J1253−0312, keep photons
inside a projected radius of $4.585\,\mathrm{kpc}$ and measure their velocities
relative to C II $1334.53\,\text{Å}$. The binning command first counts photons in
232 fine velocity bins. It normalizes the spectrum over the fitting window, then
assigns flux to each of the 50 observed pixels according to how much of each bin
falls within that pixel.

To practice binning, use the CPU build from the [first C II simulation](getting-started.md)
with the bundled synthetic configuration. The observed J1253−0312 fit uses its own
radial clump catalogues and source parameters.

```bash
python3 -m pip install numpy
python3 peacock.py run --line CII1334 --backend cpu --nphot 20000 --output run/cii-binning
python3 cii-dnn-example.py bin cii-dnn-fit-data.npz run/cii-binning cii-binned.npz
```

(j1253-training)=
### 3. Train on parameter and spectrum pairs

Each training example pairs a wind with the spectrum it produces. The J1253−0312 library
contains 2,000 winds, each simulated with 120,000 photons. One row of the training
data gives $A$, $q$ and $\log_{10}N_1$, and its matching row gives the spectrum on the
fine velocity grid. The download already contains the trained network, so you can
[run the fit](#run-a-new-fit) immediately.

```{raw} html
<details><summary>Build a model library and train your own network</summary>
```

To construct a new library for equal-size clumps, turn the encounter rate $\kappa(r)=A(r/r_0)^{-q}$
into a number density by dividing by the clump cross section $\pi R_{\mathrm{cl}}^2$, with
$r_0=1\,\mathrm{kpc}$. Integrate the density over the halo to obtain the clump count. The supplied
FCC generator, `tools/fcc_clump_geometry.py`, takes that count with `--n-clouds` and the slope
with `--volume-beta`.

Pass the complete position file to `peacock.py run` with `--clump-file`. In
the cloud section, set the reference lower-level C II column to $10^\ell\,\mathrm{cm}^{-2}$,
where $\ell=\log_{10}(N_1/\mathrm{cm}^{-2})$. Run and
bin one spectrum for each parameter row. Stack the fine spectra in the same row order as
the parameters and save them as `theta` and `fine` in `library.npz`. Recreating the archived
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

```{raw} html
</details>
```

(j1253-fit)=
### 4. Fit the observed spectrum

To reproduce the spectrum shown above, run the replay. It evaluates the trained
network at the 3,606 wind models saved from the original fit, applies the adopted
velocity shift and continuum scale, and compares each prediction with the data on
the observed velocity grid. The output CSV includes the highest-likelihood
spectrum and the two independent simulations used to check it.

```bash
python3 cii-dnn-example.py replay cii-dnn-fit-data.npz --output cii-comparison.csv
```

#### Run a new fit

How well does the observed C II profile constrain the wind? Start with the
{download}`fitting script <assets/research/cii-dnn-example.py>` and
{download}`J1253−0312 data and trained network <assets/research/cii-dnn-fit-data.npz>`
in the same directory. The `fit` command draws fresh samples using the saved
network. It runs on a CPU with the following commands.

```bash
python3 -m pip install "dynesty==3.2.0" matplotlib
python3 cii-dnn-example.py fit cii-dnn-fit-data.npz --seed 17 --output run/j1253-seed17
```

The priors describe which winds the fit considers before seeing the galaxy's
spectrum. The three parameters vary independently at this stage.

| Wind parameter | Prior for J1253−0312 |
| --- | --- |
| Clump encounter rate $A$ at 1 kpc | 1–9 kpc⁻¹, uniform in the logarithm. The ranges 1–3 and 3–9 kpc⁻¹ have equal prior probability. |
| Radial slope $q$ | 1–3, dimensionless and uniform across this range. Larger values put more of the encounters toward the inner wind for a given $A$. |
| C II column through one clump radius | $\ell=\log_{10}(N_1/\mathrm{cm}^{-2})$ is uniform from 14.3 to 15.3. |

The fit compares the predicted and observed flux in each pixel, giving less
weight to pixels with larger uncertainty. Open `corner.png` to see which winds
the data favor. Read down its first column to see how changes in the encounter
rate can be offset by changes in the other parameters.

```{figure} assets/research/cii-j1253-posterior-corner.png
:alt: Posterior distributions for A, q and the logarithmic C II column. The upward slope of the A–q contours shows that larger encounter rates at one kiloparsec are favored together with steeper radial declines.
:width: 85%

J1253−0312 C II fit with seed 17. Dashed lines on the diagonal mark the 16th,
50th and 84th percentiles. The contours enclose approximately 68% and 95% of the
joint posterior for each pair. The upward slope in the $A$–$q$ panel shows that
a higher clump encounter rate at 1 kpc can compensate for a steeper decline with
radius in this wind model.
```

To check sensitivity to the sampling seed, repeat the fit in a fresh output
directory with the same network, data, priors and sampler settings.

```bash
python3 cii-dnn-example.py fit cii-dnn-fit-data.npz --seed 43 --output run/j1253-seed43
```

Each entry below is the posterior median with its equal-tailed 16th–84th
percentile interval.

| Parameter | Seed 17 | Seed 43 |
| --- | --- | --- |
| $A$ (kpc⁻¹) | 5.58 [3.08, 7.26] | 5.63 [3.21, 7.32] |
| $q$ | 1.594 [1.234, 1.836] | 1.606 [1.276, 1.820] |
| $\log_{10}(N_1/\mathrm{cm}^{-2})$ | 14.653 [14.506, 14.909] | 14.644 [14.497, 14.907] |

All three medians shifted by less than 2.4% of their seed-17 interval widths.
Both runs give a broad range of allowed $A$ and the same positive correlation
between $A$ and $q$. Download the weighted samples for
{download}`seed 17 <assets/research/cii-j1253-posterior-seed17.npz>` or
{download}`seed 43 <assets/research/cii-j1253-posterior-seed43.npz>` to examine
these distributions. Column order is recorded in `parameter_names`.

```{raw} html
<details><summary>How the sampler draws and weights the models</summary>
```

Starting from independent uniform coordinates $u_1,u_2,u_3$ between zero and
one, the script uses $A=9^{u_1}\,\mathrm{kpc}^{-1}$, $q=1+2u_2$, and
$\ell=14.3+u_3$. The prediction function takes $A$ in physical units and
applies the logarithm internally. The fit uses a Gaussian likelihood with a
fixed variance in each pixel, combining observational uncertainty with the
estimated Monte Carlo variance in the training library.

The static sampler starts with 300 live points (trial winds) and stops when the
estimated remaining change in log evidence falls below `dlogz=0.05`.
`posterior.npz` stores the sampled winds and their normalized posterior weights.
Both the [corner plot](https://dynesty.readthedocs.io/en/v3.2.0/quickstart.html#corner-plots)
and the percentiles in `summary.json` use those weights. In the script,
`results.importance_weights()` supplies them to `dynesty.utils.quantile`.

```{raw} html
</details>
```

(j1253-validation)=
### 5. Rerun transport at the fitted parameters

The maximum-likelihood point from the archived fit has $A=6.375\,\mathrm{kpc}^{-1}$,
$q=1.685$ and $\log_{10} N_1=14.576$. Keep the cloud
geometry, source and observing settings fixed, then change the photon seeds and rerun the
full simulation. Bin both direct spectra with the same aperture, normalization, velocity
shift, pixel edges and flux scale as the DNN prediction.

How close is the network prediction? At the archived best fit, the difference
from the mean of two independent 120,000-photon spectra is comparable to the
simulations' own sampling noise. Across the observed pixels the RMS difference
is $1.01\times10^{-5}$ in normalized flux-density units. Expressed in units of each
pixel's Monte Carlo uncertainty, the RMS is 1.11. The replay CSV contains both
simulations, their mean and the difference from the network at each velocity.

This comparison checks the predicted spectrum at one wind model. Before fitting
the observations, the study also checked predictions at 16 other parameter
points, using two independent simulations at each.

For a new fit, save two copies of your best-fit configuration as `fit-seed-a.cfg`
and `fit-seed-b.cfg`. Use the same grid seed in both, give each a different photon
seed, and supply your complete best-fit clump catalogue (called `fit-clumps.txt` below).
Then generate and bin the two spectra:

```bash
python3 peacock.py run --line CII1334 --backend cpu --config fit-seed-a.cfg --clump-file fit-clumps.txt --nphot 120000 --output run/cii-check-a
python3 peacock.py run --line CII1334 --backend cpu --config fit-seed-b.cfg --clump-file fit-clumps.txt --nphot 120000 --output run/cii-check-b
python3 cii-dnn-example.py bin cii-dnn-fit-data.npz run/cii-check-a cii-check-a.npz
python3 cii-dnn-example.py bin cii-dnn-fit-data.npz run/cii-check-b cii-check-b.npz
```
