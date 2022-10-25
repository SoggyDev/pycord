#
# pycord documentation build configuration file, created by
# sphinx-quickstart on Fri Aug 21 05:43:30 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys
from importlib.metadata import version as get_version

old_changelog = os.path.join(os.path.dirname(__file__), "..", "CHANGELOG.md")
new_changelog = os.path.join(os.path.dirname(__file__), "changelog.md")

with open(old_changelog) as f:
    changelog_lines = f.readlines()

# Inject relative documentation links
for i, line in enumerate(changelog_lines):
    if line.startswith("[version guarantees]: "):
        changelog_lines[i] = "[version guarantees]: version_guarantees.rst\n"
        break

CHANGELOG_TEXT = (
    "".join(changelog_lines)
    + """
## Older Versions

A changelog for versions prior to v2.0 can be found [here](old_changelog.rst).
"""
)

with open(new_changelog) as fr:
    if fr.read() != CHANGELOG_TEXT:  # Only write if it's changed to avoid recompiling
        with open(new_changelog, "w") as fw:
            fw.write(CHANGELOG_TEXT)

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(".."))
sys.path.append(os.path.abspath("extensions"))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "builder",
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.duration",
    "sphinxcontrib_trio",
    # "details",
    "exception_hierarchy",
    "attributetable",
    "resourcelinks",
    "nitpick_file_ignorer",
    "myst_parser",
    "sphinx_copybutton",
    "sphinxext.opengraph",
]

toc_object_entries_show_parents = "hide"

ogp_site_url = "https://pycord.dev/"
ogp_image = "https://pycord.dev/static/img/logo.png"

autodoc_member_order = "bysource"
autodoc_typehints = "none"
# maybe consider this?
# napoleon_attr_annotations = False

extlinks = {
    "issue": ("https://github.com/Pycord-Development/pycord/issues/%s", "GH-"),
    "dpy-issue": ("https://github.com/Rapptz/discord.py/issues/%s", "GH-"),
}

# Links used for cross-referencing stuff in other documentation
intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
    "aio": ("https://docs.aiohttp.org/en/stable/", None),
    "req": ("https://requests.readthedocs.io/en/latest/", None),
}

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |maybecoro| replace:: This function *could be a* |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
"""

# Add any paths that contain templates here, relative to this directory.
# templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = {
    ".rst": "restructuredtext",  # Used For The Other Docs
    ".md": "markdown",  # Used ONLY In the Guide For Faster Making Time
}

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "Pycord"
copyright = "2015-2021, Rapptz & 2021-present, Pycord Development"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#

# The full version, including alpha/beta/rc tags.
release = get_version("py-cord")

# The short X.Y version.
version = ".".join(release.split(".")[:2])

# This assumes a tag is available for final releases
branch = (
    "master"
    if "a" in version or "b" in version or "rc" in version or "dev" in release
    else f"v{release}"
)

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

gettext_compact = False

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "node_modules"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "friendly"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# Nitpicky mode options
nitpick_ignore_files = [
    "migrating_to_v1",
    "whats_new",
]

# -- Options for HTML output ----------------------------------------------

html_experimental_html5_writer = True

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "furo"

html_context = {
    "discord_invite": "https://pycord.dev/discord",
    "discord_extensions": [
        ("discord.ext.commands", "ext/commands"),
        ("discord.ext.tasks", "ext/tasks"),
        ("discord.ext.pages", "ext/pages"),
        ("discord.ext.bridge", "ext/bridge"),
    ],
}

resource_links = {
    "discord": "https://pycord.dev/discord",
    "issues": "https://github.com/Pycord-Development/pycord/issues",
    "discussions": "https://github.com/Pycord-Development/pycord/discussions",
    "examples": f"https://github.com/Pycord-Development/pycord/tree/{branch}/examples",
    "guide": "https://guide.pycord.dev/",
}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
base_colors = {
    "white": "#ffffff",
    "grey-1": "#f9f9fa",
    "grey-1-8": "rgba(249, 249, 250, 0.8)",
    "grey-2": "#ededf0",
    "grey-3": "#d7d7db",
    "grey-4": "#b1b1b3",
    "grey-5": "#2a2a2b",
    "grey-6": "#4a4a4f",
    "grey-7": "#2a2a2b",
    "grey-8": "#1e1e1f",
    "black": "#0c0c0d",
    "blue-1": "#3399ff",
    "blue-2": "#0a84ff",
    "blue-3": "#0060df",
    "blue-4": "#003eaa",
    "blue-5": "#002275",
    "blue-6": "#000f40",
    "blurple": "#7289da",
}

html_theme_options = {
    "source_repository": "https://github.com/Pycord-Development/pycord",
    "source_branch": "master",
    "source_directory": "docs/",
    "light_css_variables": {
        # Theme
        # "color-brand-primary": "#5865f2",
        "font-stack": "'Outfit', sans-serif",
        # Custom
        **base_colors,
        "attribute-table-title": "var(--grey-6)",
        "attribute-table-entry-border": "var(--grey-3)",
        "attribute-table-entry-text": "var(--grey-5)",
        "attribute-table-entry-hover-border": "var(--blue-2)",
        "attribute-table-entry-hover-background": "var(--grey-2)",
        "attribute-table-entry-hover-text": "var(--blue-2)",
        "attribute-table-badge": "var(--grey-7)",
        "light-snake-display": "unset",
        "dark-snake-display": "none",
    },
    "dark_css_variables": {
        # Theme
        # "color-foreground-primary": "#fff",
        # "color-brand-primary": "#5865f2",
        # "color-background-primary": "#17181a",
        # "color-background-secondary": "#1a1c1e",
        # "color-background-hover": "#33373a",
        # Custom
        "attribute-table-title": "var(--grey-3)",
        "attribute-table-entry-border": "var(--grey-5)",
        "attribute-table-entry-text": "var(--grey-3)",
        "attribute-table-entry-hover-border": "var(--blue-1)",
        "attribute-table-entry-hover-background": "var(--grey-6)",
        "attribute-table-entry-hover-text": "var(--blue-1)",
        "attribute-table-badge": "var(--grey-4)",
        "light-snake-display": "none",
        "dark-snake-display": "unset",
    },
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "./images/pycord_logo.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "./images/pycord.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_js_files = ["js/custom.js"]

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = "_static/scorer.js"

# html_js_files = ["custom.js", "settings.js", "copy.js", "sidebar.js"]

# Output file base name for HTML help builder.
htmlhelp_basename = "pycorddoc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #'preamble': '',
    # Latex figure (float) alignment
    #'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    ("index", "Pycord.tex", "Pycord Documentation", "Pycord Development", "manual"),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [("index", "Pycord", "Pycord Documentation", ["Pycord Development"], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        "Pycord",
        "Pycord Documentation",
        "Pycord Development",
        "Pycord",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False


linkcheck_ignore = [
    r"https://discord.com/developers/docs/.*#",
    r"https://support(?:-dev)?.discord.com/hc/en-us/articles/.*",
    r"https://dis.gd/contact",
]
