# Spectral fitting

Fit observed ultraviolet spectra using a neural-network surrogate trained on PEACOCK
radiative transfer calculations.

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
