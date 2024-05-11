from setuptools import setup, find_packages

setup(
    name='ArchNetAI',
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    version='0.1.0',
    license='Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International',
    description='Python library that leverages the Ollama API for generating AI-powered content.',
    author='UgurkanTech',
    install_requires=['instructor', 'numpy', 'ollama', 'openai', 'pydantic'],
    tests_require=['pytest'],
    
)
