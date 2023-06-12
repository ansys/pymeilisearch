.. _ref_contributing:

Contributing
============

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with it and all `Coding style <dev_guide_coding_style_>`_ before attempting to
contribute to pymeilisearch.
 
The following contribution information is specific to pymeilisearch.


Cloning the pymeilisearch repository
------------------------------------

Run this code to clone and install the latest version of pymeilisearch in development mode:

.. code:: console

    git clone https://github.com/pyansys/pymeilisearch
    cd pymeilisearch
    pip install pip -U
    pip install -e .


Posting issues
--------------

Use the `pymeilisearch Issues <pymeilisearch_issues_>`_
page to submit questions, report bugs, and request new features. When possible,
use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these categories, create your own issue.

To reach the project support team, email `Pyansys core <pyansys.core@ansys.com>`_.

Viewing pymeilisearch documentation
-----------------------------------

Documentation for the latest stable release of pymeilisearch is hosted at
`pymeilisearch Documentation <pymeilisearch_docs_>`_.

In the upper right corner of the documentation's title bar, there is an option
for switching from viewing the documentation for the latest stable release
to viewing the documentation for the development version or previously
released versions.


Code style
----------

pymeilisearch follows PEP8 standard as outlined in the `PyAnsys Development Guide
<PyAnsys Developer's guide_>`_ and implements style checking using
`pre-commit <precommit_>`_.

To ensure your code meets minimum code styling standards, run::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks. For example::

  $ pre-commit install
  $ git commit -am "FEAT: added the new feature"
  blacken-docs.............................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
  check for merge conflicts................................................Passed
  debug statements (python)................................................Passed
  Validate GitHub Workflows................................................Passed
  prettier.................................................................Passed


.. _precommit: https://pre-commit.com/
.. _dev_guide_contributing: https://dev.docs.pyansys.com/how-to/contributing.html
.. _dev_guide_coding_style: https://dev.docs.pyansys.com/coding-style/index.html
.. _PyAnsys Developer's guide: https://dev.docs.pyansys.com/
.. _pymeilisearch_docs: https://pymeilisearch.docs.ansys.com/version/stable/
.. _pymeilisearch_issues: https://github.com/ansys/pymeilisearch/issues
.. _getting_started: https://pymeilisearch.docs.ansys.com/version/stable/getting-started/index.html
.. _user_guide: https://pymeilisearch.docs.ansys.com/version/dev/user-guide/index.html


