import os
import sys
from distutils.command.build import build
from setuptools import setup
from setuptools.command.test import test
from setuptools.command.install import install
import snimpy

rtd = os.environ.get('READTHEDOCS', None) == 'True'


class SnimpyTestCommand(test):
    def run_tests(self, *args, **kwds):
        # Ensure we keep a reference to multiprocessing and pysnmp to
        # avoid errors at the end of the test
        import multiprocessing
        import pysnmp
        SnimpyTestCommand.multiprocessing = multiprocessing
        SnimpyTestCommand.pysnmp = pysnmp
        return test.run_tests(self, *args, **kwds)


if __name__ == "__main__":
    readme = open('README.rst').read()
    history = open('HISTORY.rst').read().replace('.. :changelog:', '')

    setup(name="snimpy",
          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: System Administrators',
              'License :: OSI Approved :: ISC License (ISCL)',
              'Operating System :: POSIX',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 3',
              'Topic :: System :: Networking',
              'Topic :: Utilities',
              'Topic :: System :: Monitoring'
          ],
          url='https://github.com/vincentbernat/snimpy',
          description=snimpy.__doc__,
          long_description=readme + '\n\n' + history,
          author=snimpy.__author__,
          author_email=snimpy.__email__,
          packages=["snimpy"],
          entry_points={
              'console_scripts': [
                  'snimpy = snimpy.main:interact',
              ],
          },
          data_files=[('share/man/man1', ['man/snimpy.1'])],
          zip_safe=False,
          cffi_modules=["snimpy/smi_build.py:ffi"],
          install_requires=["cffi >= 1.0.0", "pysnmp >= 4", "setuptools"],
          setup_requires=["cffi >= 1.0.0", "vcversioner"],
          tests_require=list(filter(None, ["cffi >= 1.0.0",
                                           "pysnmp >= 4",
                                           "nose",
                                           "mock",
                                           sys.version_info < (2, 7) and
                                           "unittest2"])),
          test_suite="nose.collector",
          cmdclass={
              "test": SnimpyTestCommand
          },
          vcversioner={
              'version_module_paths': ['snimpy/_version.py'],
          },
          )
