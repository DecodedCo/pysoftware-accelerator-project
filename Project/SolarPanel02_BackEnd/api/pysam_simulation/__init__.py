from pathlib import Path
from . import PySSC

SSC_FILES_ROOT = str(Path(__file__).parent)

ssc = PySSC.PySSC(SSC_FILES_ROOT)
