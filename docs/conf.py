import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

project = "FASTA Reader"
language = "ru"
extensions = ["sphinx.ext.autodoc"]
html_theme = "alabaster"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]