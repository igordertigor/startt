from pybuilder.core import use_plugin, init
from pybuilder.vcs import count_travis

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "startt"
default_task = "publish"
version = '0-{}'.format(count_travis())

with open('src/main/python/startt/__init__.py', 'w') as f:
    f.write('''# This file is automatically written during the build process
# Do not edit manually!
version = "{}"
'''.format(version))


@init
def set_properties(project):
    project.depends_on('docopt')
    project.depends_on('jinja2')
