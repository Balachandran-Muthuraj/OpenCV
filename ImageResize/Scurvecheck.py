import pandas as pd

# Load the Excel file
file_path = "Book2.xlsx"
sheet1 = pd.read_excel(file_path, sheet_name="Sheet1")
sheet2 = pd.read_excel(file_path, sheet_name="Sheet2")

# Ensure both sheets have the same shape
if sheet1.shape != sheet2.shape:
    print("Sheets have different shapes!")
else:
    differences = sheet1 != sheet2
    changed_cells = []

    for row in range(sheet1.shape[0]):
        for col in range(sheet1.shape[1]):
            if differences.iloc[row, col]:
                val1 = sheet1.iloc[row, col]
                val2 = sheet2.iloc[row, col]
                change_type = "less in Sheet2" if pd.to_numeric(val2, errors='coerce') < pd.to_numeric(val1, errors='coerce') else "changed"
                changed_cells.append({
                    "Row": row + 1,
                    "Column": sheet1.columns[col],
                    "Sheet1 Value": val1,
                    "Sheet2 Value": val2,
                    "Type": change_type
                })

    # Print the differences
    if changed_cells:
        for change in changed_cells:
            print(change)
    else:
        print("No differences found.")
