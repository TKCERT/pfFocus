from setuptools import setup
import os.path

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        with open(filepath, 'r') as fh:
            return fh.read()
    except IOError:
        return ''

setup(
    name='pfFocus',
    version='0.1',
    description='Generate meaningful output from your pfSense configuration backup',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='thyssenkrupp CERT',
    author_email='tkag-cert@thyssenkrupp.com',
    license='GPL-V3',
    url='https://github.com/TKCERT/pfFocus',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: Text Editors :: Documentation',
        'Topic :: Text Processing'],
    py_modules=[
        'pf_focus.util',
        'pf_focus.pfsense',
        'pf_focus.progress',
        'pf_focus.parse',
        'pf_focus.format',
        'pf_focus.bbcode',
        'pf_focus.markdown',
    ],
    entry_points = {
        'console_scripts': [
            'pf-parse=pf_focus.parse:main',
            'pf-format=pf_focus.format:main',
            'pfFocus-parse=pf_focus.parse:main',
            'pfFocus-format=pf_focus.format:main',
        ]
    },
    install_requires=read_file('requirements.txt').splitlines(),
    include_package_data=True,
)
