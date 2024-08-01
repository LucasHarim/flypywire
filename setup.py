
from distutils.core import setup

setup(name='jsbsimpy',
      version='1.0',
      description='Exploring JSBSim and ZeroMQ functionalities',
      author='Lucas Harim G. C.',
      author_email='harimlgc@usp.br',
      packages = ['jsbsimpy'],
    install_requires = [
      'numpy',
      'jsbsim',
      'matplotlib',
      'PyQt5',
      'pyzmq',
      'zmq-requests @ git+https://github.com/LucasHarim/zmq-requests@main']
     )