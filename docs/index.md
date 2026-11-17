# PEACOCK

PEACOCK (Profiles of Emission and Absorption from Clumpy Outflows with Complex Kinematics) models how galactic winds shape ultraviolet emission and absorption lines. Each simulation starts with an intrinsic source spectrum and a [wind model](models.md#basic-model-parameters) that describes the clump distribution, velocity field, ion column densities, and dust content. PEACOCK then uses three-dimensional Monte Carlo radiative transfer to follow photons through the wind and generate line profiles for comparison with observations.

(overview-start)=
(use-peacock)=
(your-first-spectrum)=
## Generate your first spectrum

```{raw} html
<span id="getting-started"></span>
```

1. [Download and install PEACOCK](installation.md) on Linux, macOS or Windows.
2. [Run the C II tutorial](getting-started.md) to simulate light passing through a wind and plot the spectrum that escapes.
3. [Choose a line and an observable](choosing-a-line-and-an-observable.md) to try another transition or see how the same wind looks through a smaller aperture.

(overview-research)=
## UV line formation in clumpy winds

```{figure} assets/transport.svg
:alt: Schematic photon paths through gas clouds around a central source.
:class: home-transport
:align: center

Photon transport in a clumpy wind
```

### Model bulk outflow and random gas motions

Set the speed at which clumps move away from the galaxy and the spread in their individual velocities. Gas motions inside each clump can broaden the line further.

### Model absorption and re-emission together

A photon absorbed by a clump can be re-emitted in the same transition or, for some ions, at a different wavelength through fluorescence. PEACOCK follows both through the same wind.

### Assess what line profiles reveal about the wind

Different arrangements of clumps can produce similar spectra when the whole halo is observed at once. Compare several transitions or vary the observing aperture to see which wind models still agree with the data.

(overview-fitting)=
## Fit observed spectra

A neural network learns from simulated spectra so you can compare many wind models with an observed line. Once you find a fit, you can run PEACOCK at those parameters to check the predicted spectrum.

[Explore observed line profiles](examples.md#example-spectra) or [follow the C II fit to J1253−0312](fitting.md).

```{toctree}
:caption: Get started
:maxdepth: 2
:hidden:

installation
getting-started
choosing-a-line-and-an-observable
```

```{toctree}
:caption: Model the wind
:maxdepth: 2
:hidden:

models
configuring-a-peacock-simulation
```

```{toctree}
:caption: Examples and fitting
:maxdepth: 2
:hidden:

examples
fitting
```

```{toctree}
:caption: Reference
:maxdepth: 2
:hidden:

outputs
gpu
troubleshooting
download
citing
```
