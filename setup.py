from os import system
from os.path import dirname, join
from setuptools import setup, find_packages
from distutils.core import Command
import {{ project_name }}

install_requires = [
    'Django==1.6',
    'South==0.8.3',
    'hiredis',
    'redis==2.8.0',
    'sorl-thumbnail==11.12',
    'templatefinder',
    'django-redis==3.3',
    'raven==3.5.2',
    'Pillow==2.2.1',
    'uwsgi==1.9.20',
    'markdown2==2.1.0',
]

tests_require = [
    'nose',
    'coverage',
    'mock'
]

setup_requires = []

with open('README.rst') as readmefile:
    long_description = readmefile.read()


class BumpVersion(Command):
    description = "Bump version automatically (by your CI tool)"
    user_options = [
        ('commit', None, 'Commit changed files to VCS (no push)'),
        ('tag', None, 'Create release tag in VCS (no push)'),
    ]
    boolean_options = ['commit', 'tag']

    def initialize_options(self):
        self.commit = False
        self.tag = False

    def finalize_options(self):
        pass

    def run(self):
        v = {{ project_name }}.__version__
        new_version = v[:-1] + (v[-1] + 1, )
        new_version_str = '.'.join(map(str, new_version))
        initfile = join(dirname({{ project_name }}.__file__), '__init__.py')

        with open(initfile, 'r') as ifile:
            print "Reading old package init file..."
            istr = ifile.read()
            istr = istr.replace(str(v), str(new_version))

        with open(initfile, 'w') as ifile:
            print "Writing new init file with version %s..." % new_version_str
            ifile.write(istr)

        if self.commit:
            print "Committing version file to VCS..."
            system('git commit %s -m "Version bump %s"' % (initfile, new_version_str))

        if self.tag:
            print "Creating tag r/%s in VCS..." % new_version_str
            system('git tag r/%s' % new_version_str)


class MakeStatic(Command):
    description = "Compile LESS files into CSS, combine javascripts etc"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        params = {
            'pth': '{{ project_name }}/project_static',
            'lessc_opts': '--yui-compress --verbose -O2',
            'xjs_opts': ''
        }
        system('lessc %(lessc_opts)s %(pth)s/less/master.less %(pth)s/css/master.css' % params)
        system('r.js %(xjs_opts)s -o %(pth)s/_dev/build.js' % params)


setup(
    name='{{ project_name }}',
    version={{ project_name }}.__versionstr__,
    description='{{ project_name }}',
    long_description=long_description,
    author='Sanoma Online Dev',
    author_email='online-dev@sanomamedia.cz',
    maintainer='Michal Dub',
    maintainer_email='Michal.Dub@sanomamedia.cz',
    license='Proprietal',
    #url='',

    packages=find_packages(
        where='.',
        exclude=('docs', 'tests',)
    ),
    include_package_data=True,

    cmdclass={
        'bump_version': BumpVersion,
        'make_static': MakeStatic
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Proprietal",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires=install_requires,
    test_suite='nose.collector',
    tests_require=tests_require,
    setup_requires=setup_requires,
    entry_points={
        'console_scripts': [
            '{{ project_name }}_manage = {{ project_name }}.custom_manage:main',
        ],
    },
)
