import setuptools

REQUIRED = [
    'numpy',
    'nibabel',
    'scipy',
    'matplotlib',
    'pandas',
]

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()
    setuptools.setup(
        name = 'morphontogeny',
        version = '0.1.2',
        author = 'BioProtean Labs',
        description = 'Analysis scripts for morphometry and spacial transcriptomic data.',
        long_description = LONG_DESCRIPTION,
        long_description_content_type ='text/markdown',
        url = 'http://bioprotean.org/',
        packages = setuptools.find_packages(),
        python_requires = '>=3.5',
        install_requires = REQUIRED,
        classifiers = ["Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent"]
    )