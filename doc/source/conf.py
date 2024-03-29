"""Sphinx documentation configuration file."""

from datetime import datetime
import os

from ansys_sphinx_theme import convert_version_to_pymeilisearch, get_version_match

from ansys.tools.meilisearch import __version__

# Project information
project = "pymeilisearch"
copyright = f"(c) {datetime.now().year} ANSYS, Inc. All rights reserved"
author = "ANSYS, Inc."
release = version = __version__
cname = os.getenv("DOCUMENTATION_CNAME", "pymeilisearch.docs.ansys.com")
"""The canonical name of the webpage hosting the documentation."""

# Select desired logo, theme, and declare the html title
html_theme = "ansys_sphinx_theme"
html_short_title = html_title = project
html_theme_options = {
    "github_url": "https://github.com/ansys/pymeilisearch",
    "show_prev_next": False,
    "show_breadcrumbs": True,
    "switcher": {
        "json_url": f"https://{cname}/versions.json",
        "version_match": get_version_match(__version__),
    },
    "check_switcher": False,
    "use_meilisearch": {
        "api_key": os.getenv("MEILISEARCH_API_PUBLIC_KEY", ""),
        "index_uids": {
            f"pymeilisearch-v{convert_version_to_pymeilisearch(__version__)}": "PyMeilisearch",
        },
    },
}

# Sphinx extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_design",
    "sphinx_jinja",
    "numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3.11/", None),
}

# numpydoc configuration
numpydoc_show_class_members = False
numpydoc_xref_param_type = True

# Consider enabling numpydoc validation. See:
# https://numpydoc.readthedocs.io/en/latest/validation.html#
numpydoc_validate = True
numpydoc_validation_checks = {
    "GL06",  # Found unknown section
    "GL07",  # Sections are in the wrong order.
    # "GL08",  # The object does not have a docstring
    "GL09",  # Deprecation warning should precede extended summary
    "GL10",  # reST directives {directives} must be followed by two colons
    "SS01",  # No summary found
    "SS02",  # Summary does not start with a capital letter
    # "SS03", # Summary does not end with a period
    "SS04",  # Summary contains heading whitespaces
    # "SS05", # Summary must start with infinitive verb, not third person
    "RT02",  # The first line of the Returns section should contain only the
    # type, unless multiple values are being returned"
}


# static path
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

source_suffix = {
    ".rst": "restructuredtext",
}

# The master toctree document.
master_doc = "index"

# Excluded documentation files
exclude_patterns = ["_autoapi_templates/index.rst"]

# -- Configure Sphinx autoapi ------------------------------------------------
BUILD_API = True if os.environ.get("BUILD_API", "true") == "true" else False
if BUILD_API:
    extensions.append("autoapi.extension")
    autoapi_type = "python"
    autoapi_dirs = ["../../src/ansys"]
    autoapi_options = [
        "members",
        "undoc-members",
        "show-inheritance",
        "show-module-summary",
    ]
    autoapi_template_dir = "_autoapi_templates"
    suppress_warnings = ["autoapi"]
    autoapi_python_use_implicit_namespaces = True
    autoapi_python_class_content = "both"

# -- Configure the examples
BUILD_EXAMPLES = True if os.environ.get("BUILD_EXAMPLES", "true") == "true" else False
if not BUILD_EXAMPLES:
    exclude_patterns.append("examples.rst")

# -- Declare the Jinja context -----------------------------------------------
jinja_contexts = {
    "main_toctree": {
        "build_api": BUILD_API,
        "build_examples": BUILD_EXAMPLES,
    },
    "install_guide": {
        "version": version if not version.endswith("dev0") else "main",
    },
}

linkcheck_ignore = [
    "https://github.com/meilisearch/docs-scraper#set-your-config-file",
]
