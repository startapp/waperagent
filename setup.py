from os import popen
from shutil import copyfile
from glob import glob
from setuptools import setup, find_packages
import setuptools
from setuptools.command import install as _install

class install(_install.install):
    def initialize_options(self):
        _install.install.initialize_options(self)
    def finalize_options(self):
        _install.install.finalize_options(self)
    def run(self):
        _install.install.run(self)
        print 'Copying config file to /etc'
        copyfile('waperagent_conf.py', '/etc/waperagent_conf.py')

setup(
    name = "waperagent",
    version = popen('./version.sh').read(),
    packages = ['waperagent'],
	scripts = glob('waperagent/nwru-*'),
    py_modules = ['waperagent/waperagent']+glob('waperagent/savetopic_generator/*'),
	author = "startapp",
	author_email = "startapp38@gmail.com",
    cmdclass = {'install': install},
)
