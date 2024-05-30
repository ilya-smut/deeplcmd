from setuptools import setup

setup(
    name='deeplcmd',
    description="DeepLCMD is a simple command line app for text and document translation with Deepl Translator API ",
    long_description=open("README.md", 'r', encoding='utf8').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/ilya-smut/deeplcmd",
    project_urls={
        "Source Code": "https://github.com/ilya-smut/deeplcmd",
    },
    author="Ilya Smut",
    author_email="ilya.smut.off.g@gmail.com",
    license="GPL-3.0 license",
    version='0.1.4',
    packages=['deeplcmd'],
    install_requires=[
        'Click',
        'Deepl'
    ],
    entry_points={
        'console_scripts': [
            'deeplcmd = deeplcmd.deeplcmd:init',
        ],
    },
)
