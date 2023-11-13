
import sys
import traceback
from view.ui.mainWindow import MainWindow


try:
    MainWindow()
except Exception as e:
    traceback_msg = traceback.format_exc()
    print(f"Erro: {e}")
    print(f"Traceback: {traceback_msg}")
    sys.exit()
    