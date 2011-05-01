# -*- coding: utf-8 -*-
#from distribute_setup import use_setuptools
#use_setuptools()

from distutils.core import setup

setup(
        name='QRCode',
        version='0.1dev',
        author=['Edoardo Batini', 'Christian Wörner'],
        author_email=['eodbat@gmail.com', 'christianworner@gmail.com'],
        packages=['qrcode', 'qrcode.test'],
        scripts=['scripts/pyqrencode'],
        url='http://pypi.python.org/pypi/QRCode/',
        license='GPL V.3',
        description='Create QR Code Symbols',
        long_description=open('README').read(),
        )
