# -*- coding: utf-8 -*-
#
# Plaso documentation build configuration file.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
#
# Valid options are documented at http://sphinx-doc.org/config.html.

from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import time

from mock import Mock as MagicMock
from sphinx import apidoc


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('..'))

import plaso
from plaso import dependencies


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.7'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]


# There are many of dependencies we can't install on readthedocs, as it's
# not possible to install any python library that has a C dependency, and
# installing non-PyPi packages requires a complicated requirements.txt,
# so instead, we need to mock them.
class Mock(MagicMock):
  # Ensure the mock sqlite method will be loaded.
  sqlite_version_info = (3, 7, 9)

  @classmethod
  def __getattr__(cls, name):
    return Mock()

  # We always have the most up to date version of everything.
  def get_version(self):
    return time.strftime('%Y%m%d')

  # We're mocking pyparsing, and some parsers use the + method in their init,
  # So mock it.
  def __add__(self, other):
    return self


modules_to_mock = list(dependencies.PYTHON_DEPENDENCIES.keys())

# We also need to mock some modules that we don't have explicit dependencies on
# so that we can generate documentation for those components. We also need
# to explicitly mock each submodule.
# TODO: Find a better way to do this
ADDITIONAL_MODULES = set([
    'artifacts.knowledge_base', 'dateutil.parser', 'dtfabric.runtime', 'dfvfs.analyzer',
    'dfvfs.credentials', 'dfvfs.file_io', 'dfvfs.helpers', 'dfvfs.lib',
    'dfvfs.path', 'dfvfs.resolver', 'dfvfs.serializer',
    'dfvfs.serializer.json_serializer', 'dfvfs.vfs', 'dfvfs.volume',
    'dfwinreg.definitions', 'efilter.protocols', 'elasticsearch',
    'elasticsearch.exceptions', 'flask', 'hachoir_core',
    'hachoir_core.config', 'hachoir_parser', 'hachoir_metadata', 'MySQLdb',
    'pyelasticsearch', 'timesketch', 'timesketch.lib',
    'timesketch.lib.datastores', 'timesketch.lib.datastores.elastic',
    'timesketch.models', 'timesketch.models.sketch',
    'timesketch.models.user', 'lz4.block'])
modules_to_mock = set(modules_to_mock).union(ADDITIONAL_MODULES)

# Readthedocs has it's own install of chardet, requests and urllib3, so remove
# them from mocking.
modules_to_mock.remove('chardet')
modules_to_mock.remove('requests')
modules_to_mock.remove('urllib3')

# There are some modules we install via pip on readthedocs that we don't need
# to mock.
PIP_INSTALLED_MODULES = set(['construct', 'pyparsing', 'six'])
modules_to_mock = set(modules_to_mock).difference(PIP_INSTALLED_MODULES)
modules_to_mock = sorted(modules_to_mock)
print('Mocking modules')
for module_name in modules_to_mock:
  print(module_name)

sys.modules.update((module_name, Mock()) for module_name in modules_to_mock)

# Options for the Sphinx Napoleon extension, which reads google style
# docstrings.
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Plaso'
# This is a built in, but also apparently a sphinx config option.
# pylint: disable=redefined-builtin
copyright = 'The Plaso Project Authors'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = plaso.__version__
# The full version, including alpha/beta/rc tags.
release = plaso.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
# language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

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
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

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

# Output file base name for HTML help builder.
htmlhelp_basename = 'Plasodoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
  # The paper size ('letterpaper' or 'a4paper').
  # 'papersize': 'letterpaper',

  # The font size ('10pt', '11pt' or '12pt').
  # 'pointsize': '10pt',

  # Additional stuff for the LaTeX preamble.
  # 'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [(
  'index', 'Plaso.tex', 'Plaso Documentation',
  'The Plaso Project Authors', 'manual'), ]

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
man_pages = [(
  'index', 'plaso', 'Plaso Documentation',
  ['The Plaso Project Authors'], 1)]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [(
  'index', 'Plaso', 'Plaso Documentation',
  'The Plaso Project Authors', 'Plaso', 'One line description of project.',
  'Miscellaneous'), ]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

def RunSphinxAPIDoc(_):
  """Run sphinx-apidoc to auto-generate documentation."""
  # sys.path.append(os.path.join(os.path.dirname(__file__)))
  current_directory = os.path.abspath(os.path.dirname(__file__))
  module = os.path.join(current_directory,"..","plaso")
  apidoc.main(['-o', current_directory, module, '--force'])

def setup(app):
  """Override Sphinx setup to trigger sphinx-apidoc."""
  app.connect('builder-inited', RunSphinxAPIDoc)