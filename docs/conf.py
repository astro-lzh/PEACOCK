"""Build the PEACOCK documentation locally and on Read the Docs."""

import os


project = "PEACOCK"
author = "Zhihui Li and collaborators"
copyright = "2026, Zhihui Li and collaborators"

extensions = ["myst_parser", "sphinx.ext.mathjax"]
source_suffix = {".md": "markdown"}
root_doc = "index"
language = "en"
exclude_patterns = ["assets/**", "requirements.txt"]

myst_enable_extensions = ["dollarmath", "colon_fence"]
myst_heading_anchors = 4
mathjax_path = "mathjax/tex-mml-svg.js"
mathjax3_config = {
    "loader": {"load": ["[tex]/boldsymbol"]},
    "tex": {"packages": {"[+]": ["boldsymbol"]}},
    "svg": {"fontCache": "local"},
}

html_theme = "sphinx_rtd_theme"
html_title = "PEACOCK documentation"
html_short_title = "PEACOCK"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "titles_only": False,
    "style_nav_header_background": "#176776",
}
html_static_path = ["_static"]
html_css_files = ["peacock.css"]
html_favicon = "assets/favicon.svg"
html_show_sourcelink = False
html_copy_source = False
html_show_copyright = False
html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "")
