from setuptools import find_packages
from distutils.core import setup

setup(name='flypywire',
      version='1.0',
      description='Client-side of flypywire, an open-source and modular flight simulator for research.',
      author='Lucas Harim G. C.',
      author_email='harimlgc@usp.br',
      packages = find_packages(),
    install_requires = [
      'numpy==1.24.4',
      'opencv-python',
      'jsbsim',
      'py-trees==0.8.3',
      'pyzmq',
      'orjson',
      'zmq-requests @ git+https://github.com/LucasHarim/zmq-requests@main']
     )