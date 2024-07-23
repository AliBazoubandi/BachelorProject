from pyspark.sql import SparkSession

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.cores", "2") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Load the Parquet file into a Spark DataFrame
parquet_file = "output_file.parquet"
df = spark.read.parquet(parquet_file)

# Show the schema of the DataFrame
print("THIS IS THE PRINT SCHEMA")
print("******************************************************************************************************************")
df.printSchema()

# Display the first few rows of the DataFrame
print("THIS IS THE DATA FRAME")
print("******************************************************************************************************************")
df.show()

# Perform basic queries
# Example 1: Filter rows where 'IN_BYTES' > 1000
print("THIS IS THE 1 EXAMPLE")
print("******************************************************************************************************************")
filtered_df = df.filter(df['IN_BYTES'] > 1000)
filtered_df.show()

# Example 2: Group by 'Attack' column and count occurrences
print("THIS IS THE 2 EXAMPLE")
print("******************************************************************************************************************")
attack_counts = df.groupBy('Attack').count()
attack_counts.show()

# Example 3: Calculate the average 'IN_BYTES' per 'PROTOCOL'
print("THIS IS THE 3 EXAMPLE")
print("******************************************************************************************************************")
avg_in_bytes = df.groupBy('PROTOCOL').avg('IN_BYTES')
avg_in_bytes.show()

# Stop the Spark session
spark.stop()