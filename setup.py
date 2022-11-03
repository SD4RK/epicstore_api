import setuptools

AUTHOR = 'SD4RK'
VERSION = '0.1.3'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='epicstore_api',
    version=VERSION,
    author=AUTHOR,
    description='An API wrapper for Epic Games Store written in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SD4RK/epicstore_api',
    license='MIT',
    include_package_data=True,
    install_requires=['requests>=2.28.1'],
    download_url=f'https://github.com/SD4RK/epicstore_api/archive/v_{VERSION}.tar.gz',
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7'
)
