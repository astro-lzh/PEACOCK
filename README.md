# PEACOCK

PEACOCK (Profiles of Emission and Absorption from Clumpy Outflows with
Complex Kinematics) models ultraviolet line transfer through clumpy
galactic winds.

[Read the documentation](https://peacock-rt.readthedocs.io/en/latest/).

This repository contains the Sphinx documentation and the
[transport source archive](docs/assets/PEACOCK-1.0.1.zip).
See [Citing PEACOCK](docs/citing.md) for the code and paper references.

The editable documentation lives in `docs/`. It uses Sphinx, MyST Markdown
and the Read the Docs theme. Figures, example data and the source archive
are bundled with the documentation. The local MathJax renderer also works
when browsing the built site offline.

## Build

Use Python 3.12 to create an environment and install the documentation
dependencies.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r docs/requirements.txt
.venv/bin/python -m sphinx -W --keep-going -b html docs site
```

The Python version used by Read the Docs is configured in `.readthedocs.yaml`.
Once this documentation is in its Git repository, import that repository
into Read the Docs and use the included configuration file.

After building, open `site/index.html` to browse the documentation locally.

## Version and citation

The current source package is **1.0.1**, which includes shared CPU/GPU C II
tutorial inputs and a spectrum plotting helper. Its transport physics and
atomic data are unchanged from 1.0. Use [CITATION.cff](CITATION.cff) for the
current version's metadata.

The original **1.0** software release is independently archived:

Li, Z., & Gronke, M. (2026). *PEACOCK: Profiles of Emission and Absorption from Clumpy Outflows with Complex Kinematics* (Version 1.0) [Computer software]. Zenodo. [https://doi.org/10.5281/zenodo.24206426](https://doi.org/10.5281/zenodo.24206426).

Machine-readable metadata are provided in [CITATION.cff](CITATION.cff).
See [Citing PEACOCK](docs/citing.md) for the methods and original `tlac`
references.

## License

PEACOCK is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version (SPDX: `GPL-3.0-or-later`). See [LICENSE](LICENSE) for the
complete terms.

This license applies to the PEACOCK software. Third-party components and
reference data retain their own notices and terms. In particular, the
bundled INI parser remains available under its upstream MIT license.

Bundled research figures and reference documents retain their existing
rights and attribution; they are not relicensed by the software license.
