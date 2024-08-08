from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql.functions import col,when
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
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

# Apply K-Means Clustering on High Traffic IPs
assembler = VectorAssembler(inputCols=["total_in_bytes", "total_out_bytes", "total_in_pkts", "total_out_pkts"], outputCol="features")
high_traffic_ips_features = assembler.transform(high_traffic_ips)

kmeans = KMeans(k=3, seed=42)
model = kmeans.fit(high_traffic_ips_features)
predictions = model.transform(high_traffic_ips_features)

# Map cluster numbers to risk levels (adjust as needed)
predictions = predictions.withColumn(
    "Risk_Category",
    when(col("prediction") == 0, "Low Risk")
    .when(col("prediction") == 1, "Medium Risk")
    .otherwise("High Risk")
)

# Select relevant columns to save
results = predictions.select(
    col("ipv4_src_addr"), 
    col("total_in_bytes"), 
    col("total_out_bytes"), 
    col("total_in_pkts"), 
    col("total_out_pkts"), 
    col("Risk_Category")
)

print("Results DataFrame Schema before saving:")
results.printSchema()
results.show(10)

# Save the results to MySQL
results.write.jdbc(url=db_url, table="ip_clusters", mode="append", properties=db_properties)

# Example 5: Protocol Usage Analysis
print("THIS IS THE PROTOCOL USAGE ANALYSIS EXAMPLE")
print("******************************************************************************************************************")
protocol_usage = df.groupBy("PROTOCOL") \
    .agg(
        functions.count("*").alias("count"),
        functions.sum("IN_BYTES").alias("total_in_bytes"),
        functions.sum("OUT_BYTES").alias("total_out_bytes")
    ) \
    .orderBy(functions.desc("count"))

protocol_usage.show()

# save in the mysql
protocol_usage.write.jdbc(url=db_url, table="protocol_usage", mode="append", properties=db_properties)

# # Example 6: Anomaly Detection
print("THIS IS THE ANOMALY DETECTION EXAMPLE")
print("******************************************************************************************************************")
# Calculate mean and standard deviation for IN_BYTES and OUT_BYTES
stats = df.select(
    functions.mean("IN_BYTES").alias("mean_in_bytes"),
    functions.stddev("IN_BYTES").alias("stddev_in_bytes"),
    functions.mean("OUT_BYTES").alias("mean_out_bytes"),
    functions.stddev("OUT_BYTES").alias("stddev_out_bytes")
).collect()[0]

mean_in_bytes = stats["mean_in_bytes"]
stddev_in_bytes = stats["stddev_in_bytes"]
mean_out_bytes = stats["mean_out_bytes"]
stddev_out_bytes = stats["stddev_out_bytes"]

# Define thresholds for anomaly detection
threshold_factor = 3  # Number of standard deviations to consider an anomaly
df = df.withColumn(
    "anomaly",
    functions.when(
        (col("IN_BYTES") > mean_in_bytes + threshold_factor * stddev_in_bytes) |
        (col("OUT_BYTES") > mean_out_bytes + threshold_factor * stddev_out_bytes),
        1
    ).otherwise(0)
)

anomalies_df = df.filter(col("anomaly") == 1)
anomalies_df.show(10)

# Save anomalies to MySQL
anomalies_df.select("IPV4_SRC_ADDR", "IN_BYTES", "OUT_BYTES", "anomaly") \
    .write.jdbc(url=db_url, table="anomalies", mode="append", properties=db_properties)

anomalies_pd_df = anomalies_df.toPandas()

# Scatter plot of anomalies
plt.figure(figsize=(12, 6))
sns.scatterplot(x='IN_BYTES', y='OUT_BYTES', data=anomalies_pd_df, color='red', label='Anomalies')
plt.xlabel('Incoming Bytes')
plt.ylabel('Outgoing Bytes')
plt.title('Scatter Plot of Anomalies')
plt.legend()
plt.show()

# Histogram of incoming bytes for anomalies
plt.figure(figsize=(12, 6))
plt.hist(anomalies_pd_df['IN_BYTES'], bins=50, color='red', alpha=0.7)
plt.xlabel('Incoming Bytes')
plt.ylabel('Frequency')
plt.title('Histogram of Incoming Bytes for Anomalies')
plt.show()

spark.stop()