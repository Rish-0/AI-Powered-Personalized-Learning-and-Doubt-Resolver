"""Entrypoint for Streamlit application.
Allows running with either `streamlit run app.py` or `streamlit run streamlit_app.py`.
"""
import runpy
from pathlib import Path

if __name__ == "__main__":
    target = Path(__file__).parent / "streamlit_app.py"
    runpy.run_path(str(target), run_name="__main__")
