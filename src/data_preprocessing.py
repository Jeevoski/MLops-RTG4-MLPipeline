import runpy
from pathlib import Path

script = Path(__file__).parent / 'pre-processing.py'
if __name__ == '__main__':
    runpy.run_path(str(script), run_name='__main__')
