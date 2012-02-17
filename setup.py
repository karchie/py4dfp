from distutils.core import setup

setup(
    name='py4dfp',
    version='0.1dev',
    classifiers = [
        'Development Status :: 3 - Alpha'
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License : OSI Approved :: BSD License',
        'Programming Language :: Python :: 2'
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
        ],
    description='Python support for WU 4dfp',
    long_description=open('README').read(),
    author='Kevin A. Archie',
    author_email='karchie@wustl.edu',
    url='http://github.com/karchie/py4dfp',
    packages=['py4dfp',],
    keywords='neuroimaging'
    )
