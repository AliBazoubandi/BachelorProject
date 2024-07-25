from pyspark.sql import SparkSession
from pyspark.sql import functions
import configparser

# Read the database configuration
config = configparser.ConfigParser()
config.read('db_config.ini')

db_url = f"jdbc:mysql://{config['mysql']['host']}/{config['mysql']['database']}"
db_properties = {
    "user": config['mysql']['user'],
    "password": config['mysql']['password'],
    "driver": "com.mysql.cj.jdbc.Driver"
}

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MyApp") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.cores", "2") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.jars", "/usr/share/java/mysql-connector-java-9.0.0.jar") \
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

# Example 4: High Traffic IP Addresses
print("THIS IS THE HIGH TRAFFIC IP ADDRESS EXAMPLE")
print("******************************************************************************************************************")
high_traffic_ips = df.groupBy("IPV4_SRC_ADDR") \
    .agg(
        functions.sum("IN_BYTES").alias("total_in_bytes"),
        functions.sum("OUT_BYTES").alias("total_out_bytes"),
        functions.sum("IN_PKTS").alias("total_in_pkts"),
        functions.sum("OUT_PKTS").alias("total_out_pkts")
    ) \
    .orderBy(functions.desc("total_in_bytes"), functions.desc("total_out_bytes"))

high_traffic_ips.show(10)

# save in the mysql
high_traffic_ips.write.jdbc(url=db_url, table="high_traffic_ips", mode="append", properties=db_properties)

spark.stop()