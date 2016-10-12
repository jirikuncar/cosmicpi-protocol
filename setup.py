import setuptools

setuptools.setup(
    name="cosmicpi-protocol",
    version="0.1.0",
    url="https://github.com/CosmicPi/cosmicpi-protocol",

    author="Jiri Kuncar",
    author_email="jiri.kuncar@gmail.com",

    description="Parser for data read from Arduino.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'click',
        'pyyaml',
        'werkzeug',
    ],

    entry_points={
        'console_scripts': [
            'cosmicpi-protocol = cosmicpi_protocol.__main__:cli',
        ],
        'cosmicpi.protocols': [
            'protocol-v1.0 = cosmicpi_protocol',
        ],
    },

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
