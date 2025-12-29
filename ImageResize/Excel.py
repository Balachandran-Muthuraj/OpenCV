import pandas as pd

# Load the Excel file
xls = pd.ExcelFile("Book1.xlsx")
df_service = xls.parse('VehicleService')

# Extract timestamp from Column1
df_service['DateTime'] = df_service['Column1'].str.extract(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
df_service['DateTime'] = pd.to_datetime(df_service['DateTime'], errors='coerce')

# Normalize vehicle numbers
df_service['VehicleNumber'] = df_service['VehicleNumber'].str.strip().str.upper()

# Get latest records per vehicle
latest_records = df_service.sort_values('DateTime').drop_duplicates('VehicleNumber', keep='last')

# Prepare lists
update_sql = []
skipped_sql = []

for _, row in latest_records.iterrows():
    vehicle_number = row['VehicleNumber']
    max_laden = row['MaxLadenWeight']
    date = row['DateTime']

    if pd.isnull(max_laden):
        continue

    if max_laden == 0:
        skipped_sql.append(f"-- SKIPPED: MaxLadenWeight = 0 for VehicleNumber = '{vehicle_number}' on {date}")
    else:
        update_sql.append(
            f"UPDATE WMS_Vehicle SET MaxLadenWeight = {int(max_laden * 1000)} "
            f"WHERE MaxLadenWeight = 0 AND UpdateRdmsS1 IS NULL AND VehicleNumber = '{vehicle_number}';"
        )

# Save update SQLs
with open("update_maxladen.sql", "w") as f:
    f.write("\n".join(update_sql))

# Save skipped records to a .sql file with comments
with open("update_maxladen_Skipped.sql", "w") as f:
    f.write("\n".join(skipped_sql))

# Print summary
print(f"✅ {len(update_sql)} update queries written to 'update_maxladen.sql'")
print(f"⚠️ {len(skipped_sql)} skipped entries written to 'update_maxladen_Skipped.sql'")
