import json
from os import system
from os.path import dirname, join
from setuptools import setup, find_packages
from distutils.core import Command
import {{ project_name }}

install_requires = [
    #'uwsgi==2.0.9',
    'gunicorn 19.2.1'
]
with open(join(dirname(__file__), 'requirements.txt')) as req_file:
    for l in req_file.readlines():
        l = l.strip()
        if l and not l.startswith('#'):
            install_requires.append(l)

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
            #'lessc_opts': '--yui-compress --verbose -O2',
            'lessc_opts': '--compress --clean-css --verbose -O2',
            'minjs_opts': '-mc'
        }
        system('lessc %(lessc_opts)s %(pth)s/less/master.less %(pth)s/css/master.css' % params)

        # minify javascript according to .../_dev/build.json to `.../js/$key.min.js`
        build_file = join(params['pth'], '_dev', 'build.json')
        js_dir = join(params['pth'], 'js')
        with open(build_file, 'r') as fp:
            for outfile, files in json.load(fp).iteritems():
                system('uglifyjs %(files)s %(opts)s -o %(output)s' % {
                    'files': ' '.join(join(params['pth'], f) for f in files),
                    'output': join(js_dir, '%s.min.js' % outfile),
                    'opts': params['minjs_opts'],
                })


setup(
    name='%(repo_name)s',
    version={{ project_name }}.__versionstr__,
    description='%(repo_name)s',
    long_description=long_description,
    author='Astrosat Media Online Dev',
    author_email='online-dev@astrosatmedia.cz',
    maintainer='Michal Dub',
    maintainer_email='Michal.Dub@astrosatmedia.cz',
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
    scripts=['manage.py'],
)
