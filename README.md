# PEACOCK

PEACOCK (Profiles of Emission and Absorption from Clumpy Outflows with
Complex Kinematics) models ultraviolet line transfer through clumpy
galactic winds.

This repository contains the Sphinx documentation and the
[transport source archive](docs/assets/PEACOCK_source_20261109_cuda14.zip).
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

## Release citation

The citation page uses the currently available public preprints. Update
the main methods reference when its revised public record is available.
Add the actual code release DOI, software authors and version after the
release has been archived.
