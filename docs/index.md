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

(model-bulk-outflow-and-random-gas-motions)=
### Connect gas motions to the absorption profile

Clumps moving toward the observer on the near side of a galaxy can absorb its light at blueshifted wavelengths. Random velocities give individual clumps different Doppler shifts, while thermal and turbulent motions broaden each clump’s own absorption profile.

(model-absorption-and-re-emission-together)=
### Trace resonant scattering and fluorescence

Resonant scattering can redirect light into the line of sight and partly fill an absorption trough. Si II, for example, can re-emit light absorbed at 1526.7 Å in that same transition or in a fluorescent line at 1533.4 Å.

(assess-what-line-profiles-reveal-about-the-wind)=
### Compare wind models across lines and apertures

Different winds can produce similar spectra when light from the whole halo is collected. Compare another transition or narrow the aperture to test whether the models still predict similar profiles. In the [C II aperture example](choosing-a-line-and-an-observable.md#how-aperture-size-affects-the-c-ii-line-profile), the smaller aperture collects less red emission from the halo, while the blue absorption trough changes little.

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
