from pathlib import Path

def mkdir(path):
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True)
    return str(p)

BASEDIR = Path(__file__).parents[1]
CHARTPATH = mkdir(BASEDIR / 'Charts')
EMBED_COLOR = 0x32a0a8