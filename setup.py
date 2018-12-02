import sys
from cx_Freeze import setup, Executable


import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

build_exe_options = {
    'packages': ['os', 'tkinter', 'pandas', 'time', 'datetime',
                 'random', 'threading', 'numpy', 'pytz'],
    'include_files': [
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
        
    ],
    'optimize': '2',
}

base = None
if sys.platform == "win32":
  base = "Win32GUI"

setup(
    name='Tiempo de reaccion',
    version='0.1',
    options={'build_exe': build_exe_options},
    executables=[Executable('reaction_main.py', base=base, shortcutName="Tiempo de reaccion", shortcutDir="DesktopFolder", )],
    author='graupv',
    author_email='gerapv92@gmail.com',
    description='Tiempo de reaccion'
)
