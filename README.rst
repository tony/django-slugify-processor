pipeline for handling slugification edgecases

|pypi| |build-status| |docs| |coverage| |license|

What are slugs?
===============

*Slugs* are URL's, typically generated from post titles, that you want to
be both human readable and a valid URL. They are SEO friendly.

Django provides a `slugify function <https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.text.slugify>`__
in ``django.utils.text.slugify`` which is also made available as a
`default filter <https://github.com/django/django/blob/1.11.4/django/template/defaultfilters.py#L232>`__.

Django slugs can be automatically generated in django models via packages
such as:

- `django-autoslug <https://pypi.python.org/pypi/django-autoslug>`__
  (`docs <https://pythonhosted.org/django-autoslug/>`__)
  (`github <https://github.com/neithere/django-autoslug>`__)
- `django-extensions <https://pypi.python.org/pypi/django-extensions>`__
  via `AutoSlugField <https://django-extensions.readthedocs.io/en/latest/field_extensions.html>`__
  (`docs <https://django-extensions.readthedocs.io/en/latest/>`__)
  (`github <https://github.com/django-extensions/django-extensions>`__)

The problem
===========

This project is based on an article from `devel.tech <https://devel.tech>`__
covering `django's import strings
<https://devel.tech/tips/n/djms3tTe/demystifying-djangos-import-strings/>`__.

Corner cases exist with slugification. For instance:

================  =============================  =============
Term              ``django.utils.text.slugify``  What you want
================  =============================  =============
C                 c (correct)                    n/a
C++               c                              cpp
C#                c                              c-sharp
================  =============================  =============

To make matters worse, if using a specialized model field like
``AutoSlugField`` from django-autoslug or django-extensions, the default
behavior may be to name the slugs for C++ and C# to "c-1", "c-2" after "c" is
taken.

Here's another case, acronyms / shorthands:

==================  =============================  ===================
Term                ``django.utils.text.slugify``  What you (may) want
==================  =============================  ===================
New York City       new-york-city                  nyc
Y Combinator        y-combinator                   yc 
Portland            portland                       pdx
Texas               texas                          tx
\$                  '' (empty)                     usd, aud, etc?
US$                 us                             usd
A$                  a                              aud
bitcoin             bitcoin                        btc
United States       united-states                  usa
League of Legends   league-of-legends              league
Apple® iPod Touch   apple-ipod-touch               ipod-touch
==================  =============================  ===================

Each website and niche has its own edge cases for slugs. So we need a solution
that can scale, where you can craft your own functions.

How django-slugify-processor helps
==================================

This builds on top of `django.utils.text.slugify`_ to handle your django
project's edgecases. By default, django-slugify-processor will be a pass
through to django's default behavior. Adding slugification functions via
your Django project's settings file allows you to adjust.

.. _django.utils.text.slugify: https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.text.slugify

Installation
============

.. code-block:: sh

   $ pip install django-slugify-processor

Configure
=========

To create a processor, create a function that accepts a string, and
returns a string. Assume this is *project/app/slugify_processors.py*:

.. code-block:: python

   def my_processor(value):
      value = value.replace('++', 'pp')
      return value

Inside of your settings, add a ``SLUGIFY_PROCESSORS`` list of strings
that points to the function. Anything that's compatible with
`import_string <https://docs.djangoproject.com/en/1.11/ref/utils/#django.utils.module_loading.import_string>`__,
in your settings file:

.. code-block:: python

   SLUGIFY_PROCESSORS = [
      'project.app.slugify_processors.my_processor'
   ]

Usage
=====

In normal django code
---------------------

Import ``slugify`` from ``django_slugify_processor.text``:

.. code-block:: python

   from django_slugify_processor.text import slugify

   print(slugify('C++'))
   > 'cpp'

Template code
-------------

django-slugify-processor is designed to override the built-in``slugify``
filter.

via load
""""""""

You can load by default via ``{% load django_slugify_processor %}``
in your template.

In your settings ``INSTALLED_APPS``:

.. code-block:: python

   INSTALLED_APPS = [
       'django_slugify_processor'
   ]

In your template:

.. code-block:: django

   {% load slugify_processor %}
   {{"C++"|slugify}}

via built-in
""""""""""""

To make this available in all templates, in the ``OPTIONS`` of your
template engine, add ``django_slugify_processor.template_tags``:

.. code-block:: python

   TEMPLATES = [{
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'OPTIONS': {
           'builtins': [
               'django_slugify_processor.templatetags.slugify_processor',
           ],
       },
   }]

From within the template file:

.. code-block:: django

   {{"C++"|slugify}}

Output should be: cpp

Models
------

For the most up to date documentation, view the documetation for the
plugin you're using (e.g. django-autoslug or django-extensions).

To use django-slugify-processor's ``slugify`` instead of django's default,
there will be a field option to use the function.

django-extensions
"""""""""""""""""

Tested with 1.9.7 (2017-11-26):

.. code-block:: python

   from django.db import models

   from django_extensions.db.fields import AutoSlugField
   from django_slugify_processors.text import slugify

   class MyModel(models.Model):
       title = models.CharField(max_length=255)
       slug = AutoSlugField(
           populate_from='title',
           slugify_function=slugify
       )

django-autoslug
"""""""""""""""

Tested with 1.9.3 (2017-11-26):

.. code-block:: python

   from django.db import models

   from autoslug import AutoSlugField
   from django_slugify_processors.text import slugify

   class MyModel(models.Model):
       title = models.CharField(max_length=255)
       slug = AutoSlugField(
           populate_from='title',
           slugify=slugify
       )

Credits
=======

- tox.ini based off DRF's (BSD 2-clause licensed)
- yapf configuration based off RTD / devel.tech's (MIT-licensed)

Project details
===============

==============  ============================================================================
python support  >= 3.6, pypy3
django support  2.2, > 3.1,
Source          https://github.com/develtech/django-slugify-processor
Docs            https://django-slugify-processor.git-pull.com
API             https://django-slugify-processor.git-pull.com/api.html
Changelog       https://django-slugify-processor.git-pull.com/history.html
Issues          https://github.com/develtech/django-slugify-processor/issues
Test Coverage   https://codecov.io/gh/develtech/django-slugify-processor
pypi            https://pypi.python.org/pypi/django-slugify-processor
Open Hub        https://www.openhub.net/p/django-slugify-processor
License         MIT
git repo        .. code-block:: bash

                   $ git clone https://github.com/develtech/django-slugify-processor.git
install stable  .. code-block:: bash

                   $ pip install django-slugify-processor
install dev     .. code-block:: bash

                   $ git clone https://github.com/develtech/django-slugify-processor.git
                   $ cd ./django-slugify-processor
                   $ pipenv install --dev --skip-lock
                   $ pipenv shell

tests           .. code-block:: bash

                   $ make test
==============  ============================================================================

.. |pypi| image:: https://img.shields.io/pypi/v/django-slugify-processor.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/django-slugify-processor

.. |docs| image:: https://github.com/develtech/django-slugify-processor/workflows/docs/badge.svg
   :alt: Docs
   :target: https://github.com/develtech/django-slugify-processor/actions?query=workflow%3Adocs

.. |build-status| image:: https://github.com/develtech/django-slugify-processor/workflows/tests/badge.svg
   :alt: Build Status
   :target: https://github.com/develtech/django-slugify-processor/actions?query=workflow%3Atests

.. |coverage| image:: https://codecov.io/gh/develtech/django-slugify-processor/branch/master/graph/badge.svg
    :alt: Code Coverage
    :target: https://codecov.io/gh/develtech/django-slugify-processor

.. |license| image:: https://img.shields.io/github/license/develtech/django-slugify-processor.svg
    :alt: License 
