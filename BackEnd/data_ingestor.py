import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Define the columns to read from the CSV
columns = ['IPV4_SRC_ADDR', 'L4_SRC_PORT', 'IPV4_DST_ADDR', 'L4_DST_PORT', 'PROTOCOL', 'IN_BYTES', 'IN_PKTS', 'OUT_BYTES', 'OUT_PKTS', 'Attack']

chunk_size = 10000 

csv_file = "/home/alibazoubandi/Downloads/NF-UQ-NIDS-v2.csv/NF-UQ-NIDS-v2.csv"
parquet_file = "output_file.parquet"

parquet_writer = None
first_chunk = True

# Read the CSV file in chunks and write to Parquet
for chunk in pd.read_csv(csv_file, usecols=columns, chunksize=chunk_size):
    table = pa.Table.from_pandas(chunk)
    
    if first_chunk:
        # Create a Parquet writer for the first chunk
        parquet_writer = pq.ParquetWriter(parquet_file, table.schema)
        parquet_writer.write_table(table)
        first_chunk = False
    else:
        # Append subsequent chunks to the Parquet file
        parquet_writer.write_table(table)

if parquet_writer:
    parquet_writer.close()
