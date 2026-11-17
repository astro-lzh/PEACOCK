# PEACOCK

PEACOCK (Profiles of Emission and Absorption from Clumpy Outflows with Complex Kinematics) is a three-dimensional Monte Carlo radiative transfer code for ultraviolet lines. It follows photons through gas clumps to predict how gas coverage, gas motion, dust and the source spectrum shape observed absorption and emission.

```{figure} assets/transport.svg
:alt: Schematic photon paths through gas clouds around a central source.
:class: home-transport
:align: center

Photon transport in a clumpy wind
```

(overview-research)=
## UV line formation in clumpy winds

### Model bulk outflow and random gas motions

Follow the radial outflow, random velocities among clumps and line broadening within each clump separately.

### Model absorption and re-emission together

Follow resonant scattering and fluorescent branches through the same gas distribution. Compare lines that respond differently to opacity, dust and the source spectrum.

### Assess what line profiles reveal about the wind

Different radial structures can produce similar integrated spectra. Compare transitions or extract spectra at different projected radii to test which wind properties the data constrain.

(overview-fitting)=
## Fit observed spectra

Radiative transfer libraries and a neural-network surrogate make it practical to explore the parameter space of a spectral fit. Direct transport at the fitted parameters provides a comparison with the surrogate prediction.

[See the fitting workflow](fitting.md).

(overview-start)=
## Use PEACOCK

Install PEACOCK, run a C II example on a CPU or GPU, and turn the escaping photons into a spectrum. Then [choose a line and an observable](choosing-a-line-and-an-observable.md) or configure your own wind.

[Get started](getting-started.md), [check installation for your computer](installation.md), [explore the physical model](models.md) or [see example spectra](examples.md).

```{toctree}
:caption: Model and examples
:maxdepth: 2
:hidden:

choosing-a-line-and-an-observable
models
configuring-a-peacock-simulation
examples
fitting
```

```{toctree}
:caption: Install and run
:maxdepth: 2
:hidden:

getting-started
installation
gpu
outputs
troubleshooting
download
```

```{toctree}
:caption: Citing PEACOCK
:maxdepth: 2
:hidden:

citing
```
