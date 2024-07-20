import pyarrow.parquet as pq

parquet_file = "/home/alibazoubandi/Desktop/BachelorProject/BackEnd/output_file.parquet"

try:
    table = pq.read_table(parquet_file)
    print(f"Number of rows: {table.num_rows}")
    print(f"Number of columns: {len(table.columns)}")
    print(f"Column names: {table.column_names}")
    print("First few rows:")
    print(table.to_pandas().head())
except Exception as e:
    print(f"Error reading Parquet file: {e}")