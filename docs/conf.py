import os
import sys

import alagitpull

# Get the project root dir, which is the parent dir of this
cwd = os.getcwd()
project_root = os.path.dirname(cwd)

# for autodoc to detect module
sys.path.insert(0, project_root)

# package data
about = {}
with open("../django_slugify_processor/__about__.py") as fp:
    exec(fp.read(), about)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'alagitpull',
    'sphinx_issues',
]

issues_github_path = about['__github__'].replace('https://github.com/', '')

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = about['__title__']
copyright = about['__copyright__']

version = '%s' % ('.'.join(about['__version__'].split('.'))[:2])
release = '%s' % (about['__version__'])

exclude_patterns = ['_build']

pygments_style = 'sphinx'

html_theme_path = [alagitpull.get_path()]
html_static_path = ['_static']
html_extra_path = ['manifest.json']
html_theme = 'alagitpull'
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'more.html',
        'searchbox.html',
    ]
}

html_theme_options = {
    'logo': "img/icons/logo.svg",
    'github_user': 'develtech',
    'github_repo': 'django-slugify-processor',
    'github_type': 'star',
    'github_banner': True,
    'projects': alagitpull.projects,
    'project_name': about['__title__'],
    'project_title': about['__title__'],
    'project_description': about['__description__'],
    'project_url': about['__docs__'],
    'show_meta_manifest_tag': True,
    'show_meta_og_tags': True,
    'show_meta_app_icon_tags': True,
}

alagitpull_internal_hosts = [
    'django-slugify-processor.devel.tech',
    'django-slugify-processor.git-pull.com',
    '0.0.0.0',
]
alagitpull_external_hosts_new_window = True

htmlhelp_basename = '%sdoc' % about['__title__']

latex_documents = [
    (
        'index',
        '{0}.tex'.format(about['__package_name__']),
        '{0} Documentation'.format(about['__title__']),
        about['__author__'],
        'manual',
    )
]

man_pages = [
    (
        'index',
        about['__package_name__'],
        '{0} Documentation'.format(about['__title__']),
        about['__author__'],
        1,
    )
]

texinfo_documents = [
    (
        'index',
        '{0}'.format(about['__package_name__']),
        '{0} Documentation'.format(about['__title__']),
        about['__author__'],
        about['__package_name__'],
        about['__description__'],
        'Miscellaneous',
    )
]

intersphinx_mapping = {
    'py': ('https://docs.python.org', None),
    'django': (
        'https://docs.djangoproject.com/en/1.11/',
        'https://docs.djangoproject.com/en/1.11/_objects/',
    ),
}
