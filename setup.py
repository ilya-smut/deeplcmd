from setuptools import setup

setup(
    name='deeplcmd',
    version='0.1.2',
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
