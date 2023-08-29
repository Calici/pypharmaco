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
      "structure"  
    ],
    install_requires=[
        
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)