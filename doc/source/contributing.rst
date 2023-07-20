.. _ref_contributing:

Contributing
============

Overall guidance on contributing to a PyAnsys library appears in the
`Contributing <dev_guide_contributing_>`_ topic
in the *PyAnsys Developer's Guide*. Ensure that you are thoroughly familiar
with this guide before attempting to contribute to PyMeilisearch.
 
The following contribution information is specific to PyMeilisearch.


Clone the repository
--------------------

To clone and install the latest version of PyMmeilisearch in development mode,
run this code:

.. code:: console

    git clone https://github.com/ansys/pymeilisearch
    cd pymeilisearch
    pip install pip -U
    pip install -e .


Post issues
-----------

Use the `PyMeilisearch Issues <pymeilisearch_issues_>`_
page to submit questions, report bugs, and request new features. When possible,
use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these template categories, create your own issue.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

View documentation
------------------

Documentation for the latest stable release of PyMeilisearch is hosted at
`PyMeilisearch documentation <pymeilisearch_docs_>`_.

In the upper right corner of the documentation's title bar, there is an option
for switching from viewing the documentation for the latest stable release
to viewing the documentation for the development version or previously
released versions.


Adhere to code style
--------------------

PyMeilisearch follows the PEP8 standard as outlined in the `PyAnsys Developer's Guide
<PyAnsys Developer's Guide_>`_ and implements style checking using
`pre-commit <precommit_>`_.

To ensure your code meets minimum code styling standards, run these commands::

  pip install pre-commit
  pre-commit run --all-files

You can also install this as a pre-commit hook by running this command::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks::

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
.. _PyAnsys Developer's Guide: https://dev.docs.pyansys.com/
.. _dev_guide_coding_style: https://dev.docs.pyansys.com/coding-style/index.html
.. _pymeilisearch_docs: https://pymeilisearch.docs.ansys.com/version/stable/
.. _pymeilisearch_issues: https://github.com/ansys/pymeilisearch/issues
.. _getting_started: https://pymeilisearch.docs.ansys.com/version/stable/getting-started/index.html
.. _user_guide: https://pymeilisearch.docs.ansys.com/version/dev/user-guide/index.html


