# Input/output utilities
import pandas as pd

def load_excel_sheets(file_path):
    sheets = pd.read_excel(file_path, sheet_name=None)
    return (
        sheets["capacity"],
        sheets["voltage"],
        sheets["dQdV"],
        sheets["dVdQ"],
    )
