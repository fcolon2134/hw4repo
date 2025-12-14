.. rocket_relations documentation master file, created by
   sphinx-quickstart on Thu Oct 30 11:22:51 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rocket_relations documentation
==============================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
Usage
=====

**rocket_relations** – Basic ideal rocket relations for calculating characteristic velocity and thrust coefficient.

The `__init__.py` file is a package that computes ideal rocket calculations. It contains modules with functions to perform these calculations.

Installation
------------

Download the source code or clone the repo locally. In the project root directory (`rocket_relations` inside HW5), open a terminal and create/activate a conda environment.

Steps:

1. Ensure you have Python installed.
2. Activate your conda environment (example: `(aste404)`):

   .. code-block:: bash

       conda activate aste404

3. Navigate to your root folder which contains `rocket_relations`.
4. Ensure you have Hatchling build installed:

   .. code-block:: bash

       mamba install hatchling build

   If that fails:

   .. code-block:: bash

       mamba install hatchling
       pip install build
       pip install -e .

Quickstart
----------

Import and use the package functions:

.. code-block:: python

    from rocket_relations.ideal import char_vel, thrust_coeff

    c_star = char_vel(1.2, 350, 3500)
    cf = thrust_coeff(1.2, 0.0125, 0.02, 10)

    print("c* =", c_star)
    print("Cf =", cf)

Documentation
-------------

You can also inspect functions with Python's built-in help:

.. code-block:: python

    import rocket_relations
    help(rocket_relations.char_vel)
    help(rocket_relations.thrust_coeff)

Tests
-----

Run pytest to check function correctness and input validation:

.. code-block:: bash

    pytest -q

Example result:

.. code-block:: none

    2 passed in 0.05s

   :caption: Rocket Relations Calculations Contents: Functions that compute ideal rocket equations

