from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_json, struct
from pyspark.sql.types import StructType, StructField, StringType

# Define the schema for the JSON data
kafkaMessageSchema = StructType([
    StructField("transactionDate", StringType(), True),
    StructField("transactionId", StringType(), True),
    StructField("atmLocation", StringType(), True)
])

# Initialize Spark session
spark = SparkSession.builder.appName("atm-visits").getOrCreate()
# Set logging level to WARN
spark.sparkContext.setLogLevel('WARN')

# Read the Kafka topic as a streaming DataFrame
atmVisitsRawStreamingDF = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:19092") \
    .option("subscribe", "atm.withdrawal") \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

# Cast each field from binary to string
atmVisitsStreamingDF = atmVisitsRawStreamingDF.selectExpr("cast(key as string) key", "cast(value as string) value")

# Parse the JSON from the 'value' column
atmVisitsParsedDF = atmVisitsStreamingDF.withColumn("value", from_json("value", kafkaMessageSchema)) \
    .select(col('value.*'))

# Select the required fields
atmVisitsStatusDF = atmVisitsParsedDF.select("transactionId", "atmLocation")

# Recreate the value column by converting the selected fields back to JSON
atmVisitsFinalDF = atmVisitsStatusDF.withColumn("value", to_json(struct("transactionId", "atmLocation")))

# Write the transformed data back to another Kafka topic
atmVisitsFinalDF.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:19092") \
    .option("topic", "atm.withdrawal.updates") \
    .option("checkpointLocation", "/tmp/kafkacheckpoint") \
    .start() \
    .awaitTermination()
