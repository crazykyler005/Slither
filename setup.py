import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = r'C:\Users\Smithy\AppData\Local\Programs\Python\Python37\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Smithy\AppData\Local\Programs\Python\Python37\tcl\tk8.6'

executables = [cx_Freeze.Executable("Slither.py")]

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


cx_Freeze.setup(name="Slither",
                version="1.1",
                options={"build_exe": {
                    "packages": ["pygame", "random", "simplejson", "time"],
                    "include_files":["apple.png", "snake_head.png", "snake_tail.png", "verisonNumber.txt",
                                     os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                                     os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                                     ]}},
                description = "Pygame snake clone project",
                executables = executables
                )