
from distutils.core import setup

setup(
        name='pagechanger',
        author='Paul Van de Vreede',
        author_email='paul@vdvreede.net',
        description='File alteration bot for programmatically altering large amount of files with Regular Expressions.',
        version='0.9.0',
        url='https://github.com/pvdvreede/page-changer',
        py_modules=['pagechanger'],
        entry_points={
            'console_scripts': [
                'pagechanger = pagechanger:main',
                ],
            }
     )
