import os
from setuptools import setup, find_packages
import sys

here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, 'onvif/version.txt')
version = open(version_path).read().strip()

requires = [
    'zeep >= 4.0.0',
    'PyYAML >= 5.4.1',
]

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Customer Service',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Telecommunications Industry',
    'Natural Language :: English',
    'Operating System :: POSIX',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Multimedia :: Sound/Audio',
    'Topic :: Utilities',
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
]

wsdl_files = [os.path.join('wsdl', item) for item in os.listdir('wsdl')]
wsdl_dst_dir = 'Lib/site-packages/wsdl' if sys.platform == 'win32' else \
               'lib/python%d.%d/site-packages/wsdl' % (sys.version_info.major,
                                                       sys.version_info.minor)

setup(
      name='onvif_zeep',
      version=version,
      description='Python Client for ONVIF Camera',
      long_description=open('README.rst', 'r').read(),
      author='Michael Mugnai',
      author_email='michael.mugnai@gmail.com',
      maintainer='Maik93',
      maintainer_email='michael.mugnai@gmail.com',
      license='MIT',
      keywords=['ONVIF', 'Camera', 'IPC'],
      url='http://github.com/Maik93/python-onvif-zeep',
      zip_safe=False,
      packages=find_packages(exclude=['docs', 'examples', 'tests']),
      install_requires=requires,
      include_package_data=True,
      data_files=[(wsdl_dst_dir, wsdl_files)],
      entry_points={
          'console_scripts': ['onvif-cli = onvif.cli:main']
          }
     )
