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
The script and data let you replay the published fit with NumPy and compare the predicted spectrum with two saved transport runs. To train a new network, follow step 3 with your own
library of model parameters and binned spectra.

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

(j1253-validation)=
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
