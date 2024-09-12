
from distutils.core import setup

setup(name='flypywire',
      version='1.0',
      description='Exploring JSBSim and ZeroMQ functionalities',
      author='Lucas Harim G. C.',
      author_email='harimlgc@usp.br',
      packages = ['flypywire'],
    install_requires = [
      'numpy==1.24.4',
      'jsbsim',
      'py-trees==0.8.3',
      'pyzmq',
      'orjson',
      'zmq-requests @ git+https://github.com/LucasHarim/zmq-requests@main']
     )