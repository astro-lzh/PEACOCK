# Citing PEACOCK

In publications using PEACOCK, please cite the version of the code used,
the main methods paper and the original `tlac` reference below. Include an
application paper when your analysis uses its results, fitting procedure or
scientific interpretation.

## Code release

### Current version: 1.0.2

Li, Z., & Gronke, M. (2026). *PEACOCK: Profiles of Emission and Absorption from Clumpy Outflows with Complex Kinematics* (Version 1.0.2) [Computer software]. [GitHub](https://github.com/astro-lzh/PEACOCK).

The [current source download](download.md) includes the common C II tutorial inputs and
spectrum plotting tool. Record **1.0.2** when using this package. The DOI below identifies
the separately archived **1.0** release.

```bibtex
@software{li_gronke_peacock_1_0_2,
  author  = {Li, Zhihui and Gronke, Max},
  title   = {{PEACOCK}: Profiles of Emission and Absorption from Clumpy Outflows with Complex Kinematics},
  year    = {2026},
  month   = nov,
  version = {1.0.2},
  url     = {https://github.com/astro-lzh/PEACOCK}
}
```

### Archived version: 1.0

Li, Z., & Gronke, M. (2026). *PEACOCK: Profiles of Emission and Absorption from Clumpy Outflows with Complex Kinematics* (Version 1.0) [Computer software]. Zenodo. [https://doi.org/10.5281/zenodo.24206426](https://doi.org/10.5281/zenodo.24206426).

Cite this DOI when using PEACOCK 1.0 and record the version with your
results. The code is available under the **GNU General Public License,
version 3 or later (`GPL-3.0-or-later`)**. Third-party components retain
their own notices and terms.

```bibtex
@software{li_gronke_peacock_1_0,
  author    = {Li, Zhihui and Gronke, Max},
  title     = {{PEACOCK}: Profiles of Emission and Absorption from Clumpy Outflows with Complex Kinematics},
  year      = {2026},
  month     = nov,
  version   = {1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.24206426},
  url       = {https://doi.org/10.5281/zenodo.24206426}
}
```

(li-2026a)=
## Main methods paper

**Li et al. (2026a)**. *Kinematically Coherent Multiphase Galactic Winds in
Star-Forming Galaxies Revealed by Unified Radiative Transfer Modeling of UV
Emission and Absorption Lines*. This public preprint describes PEACOCK and
its multi-ion radiative transfer fitting framework.
[arXiv:2603.06546v1](https://arxiv.org/abs/2603.06546v1).

## Original `tlac` framework

PEACOCK builds on the three-dimensional Monte Carlo radiative transfer code
`tlac`, developed by Max Gronke. Please credit this foundation with the
original code reference.

**Gronke & Dijkstra (2014)**. *Directional Lyα equivalent boosting – I.
Spherically symmetric distributions of clumps*. Monthly Notices of the
Royal Astronomical Society, **444**, 1095–1103.
[doi:10.1093/mnras/stu1513](https://doi.org/10.1093/mnras/stu1513),
[arXiv:1406.6709](https://arxiv.org/abs/1406.6709).

## Application papers

Cite these papers when they support the analysis or interpretation in your
work.

- **Wind kinematics and energetics.** Li et al. (2026), *The Prevalence of
  Turbulence-Regulated Multiphase Galactic Winds in Star-Forming Galaxies*.
  Relevant to analyses using the inferred wind properties, turbulence and
  energy budgets presented in that study.
  [arXiv:2603.06568v1](https://arxiv.org/abs/2603.06568v1).

- **C IV emission modeling.** Li et al. (2026), *Resonantly Scattered CIV
  Emission in Local Star-forming Galaxies: Radiative Transfer Constraints on
  High-ionization Gas in Reionization Analogs*. Relevant to analyses using
  the C IV emission fitting methods or results presented in that study.
  [arXiv:2609.11497v1](https://arxiv.org/abs/2609.11497v1).

## Atomic and dust data

The atomic model for each profile lists the reference data used for that network.
See the {download}`UV atomic and dust data notices <assets/uv-data-provenance.md>`.
