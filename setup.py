from setuptools import setup, find_packages

setup(
    name='reach4me',
    packages=find_packages(where='src'), 
    package_dir={'': 'src'},
    extras_require={
        'twilio': [
            'twilio'
        ]
    }
)