"""Setup file for the citeNet package."""
from setuptools import setup, find_packages

setup(
    name='citeNet',
    version='0.0.1',
    description='citation Network builder package',
    maintainer='Sampriti Chattopadhyay',
    maintainer_email='sampritc@andrew.cmu.edu',
    license='MIT',
    packages=["citeNet"],
    long_description='''A long multiline description.''',
    install_requires=[
        'networkx',    # NetworkX dependency
        'plotly',      # Plotly dependency
        'matplotlib',   # Matplotlib dependency
        'requests'],
)
