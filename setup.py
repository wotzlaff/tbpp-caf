import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tbpp_caf',
    version='0.0.2',
    author='Nico Strasdat',
    author_email='nstrasdat@gmail.com',
    description='Combinatorial Arcflow Model for the Temporal Bin Packing Problem with Fire-Ups',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wotzlaff/tbpp-caf',
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires='>=3.9',
)
