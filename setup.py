from setuptools import setup

setup(
    name='chord-trainer',
    version='',
    packages=['chordtrainer'],
    url='https://github.com/drewsonne/chord-trainer.git',
    license='',
    author='drew',
    author_email='drew.sonne@gmail.com',
    description='',
    entry_points={
        'console_scripts': [
            'chord-trainer=chordtrainer.cli:run'
        ]
    }
)
