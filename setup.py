from setuptools import setup

setup(
    name='deeplcmd',
    version='0.1.0',
    py_modules=['deeplcmd'],
    install_requires=[
        'Click',
        'Deepl'
    ],
    entry_points={
        'console_scripts': [
            'deeplcmd = deeplcmd:init',
        ],
    },
)
