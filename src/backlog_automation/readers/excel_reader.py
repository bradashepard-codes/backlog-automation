import pandas as pd


def read_excel(path: str) -> dict[str, list[dict]]:
    """Read all sheets from an Excel file. Returns {sheet_name: [row_dicts]}."""
    xl = pd.ExcelFile(path)
    return {
        sheet: pd.read_excel(xl, sheet_name=sheet).to_dict(orient="records")
        for sheet in xl.sheet_names
    }
