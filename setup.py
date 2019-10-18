from setuptools import setup, find_packages

setup(
    name='stupid_cpu',
    version='1.0',
    description='Control cpu usage by cgroups',
    author='di.wang',
    packages=find_packages(),
    install_requires=['cgroups==0.1.0', 'psutil==5.6.3'],
    entry_points={
        'console_scripts': [
            'run_stupid_cpu=stupid_cpu.main:main'
        ]
    },
    platforms='Linux'
)
