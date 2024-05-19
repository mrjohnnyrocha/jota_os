# jota_os/setup.py
from setuptools import setup, find_packages

setup(
    name="jota_os",
    version="0.1.0",
    packages=find_packages(include=['jota_os', 'jota_os.*']),
    install_requires=[
        # List dependencies here, if any
    ],
    entry_points={
        'console_scripts': [
            'jota-os-shell = jota_os.shell:main',
        ],
    },
)
