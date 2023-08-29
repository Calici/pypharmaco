from setuptools import setup

setup(
    name='pypharmaco',
    version='0.0.0',    
    description='A Python Package for Pharmaco Net utilities that developer uses',
    url='https://github.com/calici/pypharmaco',
    author='Jonathan Willianto',
    author_email='jo.will@calici.co',
    license='MIT',
    packages=[
      "env_parser", 
      "structure", 
      "web_socket"
    ],
    install_requires=[
        
    ]
)