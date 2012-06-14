
from distutils.core import setup

setup(
        name='page-changer',
        author='Paul Van de Vreede',
        author_email='paul@vdvreede.net',
        description='File alteration bot for programmatically altering large amount of files with Regular Expressions.',
        version='0.9.0',
        url='https://github.com/pvdvreede/page-changer',
        py_modules=['page-changer'],
        entry_points={
            'console_scripts': [
                'page-changer = page-changer:main',
                ],
            }
     )
