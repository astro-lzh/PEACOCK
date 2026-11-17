# Spectral fitting

Once you can [run and plot a synthetic spectrum](getting-started.md), you can compare
a family of wind models with an observed line. This page follows a C II fit to
J1253−0312, from a library of simulated spectra to a direct check of the fitted line shape.

(workflow)=
## From simulated spectra to a fit

The fitting workflow uses a deep neural network (DNN) to predict spectra during Bayesian
sampling. The source download provides the transport engine used to generate the spectral
library.

```{figure} assets/research/figure-15-dnn.png
:alt: Five stages of the PEACOCK spectral fitting pipeline, including a DNN surrogate and direct radiative-transfer validation.
:width: 100%
:target: _static/research/figure-15-dnn.pdf

Direct radiative-transfer calculations form the spectral library. A DNN predicts spectra for nested sampling. Targeted resampling expands the library, and a direct calculation checks the best-fit prediction.
```

1. **Generate spectra with radiative transfer**

   Sample the physical parameters and run PEACOCK at each point to build a library of emergent spectra.

2. **Train a spectral surrogate**

   Fit a deep neural network to predict spectra across the sampled parameter domain.

3. **Explore the posterior**

   Compare the predicted spectra with the observations inside a nested sampler.

4. **Refine where the fit needs more models**

   Add radiative transfer calculations where the posterior reaches a training boundary or where the surrogate needs denser coverage.

5. **Rerun the transport at the fitted parameters**

   Compare an independent Monte Carlo calculation with the predicted line shape at the same parameters.

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

The J1253−0312 example fits three quantities. $A$ sets the clump encounter rate
at one kiloparsec, $q$ sets its radial slope, and $\log_{10} N_1$ sets the C II
column through one clump radius in the reference lower level. The wind velocity law, dust,
level-population ratio, aperture, velocity shift and continuum scale are fixed.

The model uses a $1$–$10\,\mathrm{kpc}$ halo and $50\,\mathrm{pc}$ clumps. The training
set samples $A$ from $1$ to $9\,\mathrm{kpc}^{-1}$ uniformly in its logarithm,
$q$ from $1$ to $3$, and $\log_{10} N_1$ from $14.3$
to $15.3$.

(j1253-binning)=
### 2. Bin the escaped packets

The binning command reads the ASCII observer detuning and Doppler width, converts each
escape to velocity relative to C II $1334.53\,\text{Å}$, and selects photons inside a projected
aperture of $4.585\,\mathrm{kpc}$. It counts escapes in $232$ fine bins, normalizes the
spectrum over the fitting window and maps it onto the $50$ observed pixels by bin
overlap.

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

The J1253 training library used 2,000 physical parameter vectors and 120,000 launched
packets per simulation. Each row of the input matrix gives the three physical parameters.
The target row is the 232-bin spectrum after the same aperture selection and
normalization. The network learns the mapping from model parameters to emergent flux
density.

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

(j1253-fit)=
### 4. Fit the observed spectrum

The original fit used nested sampling with independent uniform priors in $\log_{10} A$,
$q$ and $\log_{10} N_1$. For each sampled point, the DNN predicts the fine-bin
spectrum. Apply the fixed velocity offset and continuum scale, integrate over the observed
pixels and compare with the measured flux. The fit used observational variance plus the
training library’s estimated packet variance.

The replay evaluates the saved network at all 3,606 archived candidate samples and
recomputes their likelihood ranking. It selects the original maximum-likelihood sample and
writes the model and data on the same velocity grid.

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

To define the prior, start with three independent uniform coordinates
$u_1,u_2,u_3$ between zero and one. The following transformation gives the
physical inputs supplied to the DNN.

| Parameter | Prior used in this fit | Value passed to the prediction function |
| --- | --- | --- |
| Clump encounter rate $A$ at 1 kpc | Uniform in $\log_{10}(A/\mathrm{kpc}^{-1})$ for $1\leq A/\mathrm{kpc}^{-1}\leq9$ | $A=9^{u_1}\,\mathrm{kpc}^{-1}$ |
| Radial slope $q$ of the encounter rate | Uniform from 1 to 3, dimensionless | $q=1+2u_2$ |
| Reference lower-level C II column through one clump radius, $\ell=\log_{10}(N_1/\mathrm{cm}^{-2})$ | Uniform from 14.3 to 15.3 in $\ell$ | $\ell=14.3+u_3$ |

The prediction function takes $A$ in physical units and applies the logarithm
internally. It maps each trial spectrum onto the 50 observed pixels. A Gaussian
likelihood compares the predicted and observed fluxes using the fixed variance
of each pixel, including observational and Monte Carlo contributions.
The tutorial uses 300 live points and the static sampler's `dlogz=0.05` stopping
criterion for the estimated remaining contribution to the log evidence.

Each run writes `posterior.npz` (parameter samples and their normalized posterior
weights), `summary.json` (weighted quantiles and run settings), and `corner.png`.
The script obtains the weights with `results.importance_weights()` and passes them
to `dynesty.utils.quantile`. The [dynesty corner plot](https://dynesty.readthedocs.io/en/v3.2.0/quickstart.html#corner-plots)
uses the same weights for the one- and two-parameter distributions.

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

(j1253-validation)=
### 5. Rerun transport at the fitted parameters

The maximum-likelihood point from the archived fit has $A=6.375\,\mathrm{kpc}^{-1}$,
$q=1.685$ and $\log_{10} N_1=14.576$. Keep the cloud
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
