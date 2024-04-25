from setuptools import setup

setup(
    name='pypharmaco',
    version='0.0.2',    
    description='A Python Package for Pharmaco Net utilities that developer uses',
    url='https://github.com/calici/pypharmaco',
    author='Jonathan Willianto',
    author_email='jo.will@calici.co',
    license='MIT',
    packages=[ 
      "pypharmaco.env_parser", 
      "pypharmaco.structure", 
      "pypharmaco.web_socket" 
    ],
    install_requires=[
        "typing_extensions>=4.7.1",
    ]
)