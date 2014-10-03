from setuptools import setup, find_packages

setup(
    name='taskwarrior-time-report',
    version='0.1.0',
    url='https://github.com/kostajh/taskwarrior-time-report',
    description=(
        'Generate timesheet reports with totals'
    ),
    author='Kosta Harlan',
    author_email='kosta@kostaharlan.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "taskw",
        "cement",
        "tabulate",
        "blessings"
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'taskwarrior_time_report = taskwarrior_time_report:cmdline'
        ],
    },
)
