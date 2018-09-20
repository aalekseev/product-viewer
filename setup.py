import sys
from cx_Freeze import setup, Executable

buildOptions = dict(
    packages=['os'],
    includes=['PyQt5', 'lxml', 'redis'],
    excludes=[])

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('product_viewer/app.py', base=base, targetName='product-viewer')
]

setup(name='product_viewer',
      version='0.1',
      description='A PyQt5 GUI app for viewing items listed in Yandex YML files',
      options=dict(build_exe=buildOptions),
      executables=executables)
