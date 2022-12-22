from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='fastapi_versionizer',
    version='0.1.0',
    author='Alex Schimpf',
    description='API versionizer for FastAPI web applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alexschimpf/fastapi-versionizer',
    packages=['fastapi_versionizer'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'fastapi>=0.56.0',
        'starlette',
        'pydantic'
    ],
    python_requires='>=3.6',
)
