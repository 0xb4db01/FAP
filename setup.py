from setuptools import setup

setup(
    name='FAP',
    description='Fake Access Point',
    author='0xb4db01',
    packages=[
        'fap',
        'fap.iptables',
        'fap.flaskaptive',
        'fap.logmon',
    ],
    entry_points={
        'console_scripts': [
            'fap=fap.fap:main',
        ]
    }
)
