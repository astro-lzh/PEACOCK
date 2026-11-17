# PEACOCK

PEACOCK (Profiles of Emission and Absorption from Clumpy Outflows with Complex Kinematics) is a three-dimensional Monte Carlo radiative transfer code for ultraviolet lines. It follows photons through gas clumps to predict how gas coverage, gas motion, dust and the source spectrum shape observed absorption and emission.

(overview-start)=
(use-peacock)=
## Your first spectrum

1. [Download and install PEACOCK](installation.md) on Linux, macOS or Windows.
2. [Run the C II tutorial](getting-started.md) to build the code, launch 100,000 photons and plot the escaping spectrum.
3. [Choose a line and an observable](choosing-a-line-and-an-observable.md) to try a different transition or extract a smaller aperture from your first run.

(overview-research)=
## UV line formation in clumpy winds

```{figure} assets/transport.svg
:alt: Schematic photon paths through gas clouds around a central source.
:class: home-transport
:align: center

Photon transport in a clumpy wind
```

### Model bulk outflow and random gas motions

Follow the radial outflow, random velocities among clumps and line broadening within each clump separately.

### Model absorption and re-emission together

Follow resonant scattering and fluorescent branches through the same gas distribution. Compare lines that respond differently to opacity, dust and the source spectrum.

### Assess what line profiles reveal about the wind

Different radial structures can produce similar integrated spectra. Compare transitions or extract spectra at different projected radii to test which wind properties the data constrain.

(overview-fitting)=
## Fit observed spectra

Radiative transfer libraries and a neural-network surrogate make it practical to explore the parameter space of a spectral fit. Direct transport at the fitted parameters provides a comparison with the surrogate prediction.

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
