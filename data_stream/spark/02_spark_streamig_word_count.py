from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Stop the existing SparkContext if it exists
try:
    sc.stop()
except:
    pass

# Create a new Spark Context with two working threads
sc = SparkContext("local[2]", "NetworkWordCount")

# Set log level to WARN to reduce verbosity
sc.setLogLevel("WARN")

# Create local StreamingContext with batch interval of 1 second
ssc = StreamingContext(sc, 1)

# Create DStream that will connect to the stream of input lines from connection to localhost:9999
lines = ssc.socketTextStream("localhost", 9999)

# Split lines into words
words = lines.flatMap(lambda line: line.split(" "))

# Count each word in each batch
pairs = words.map(lambda word: (word, 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

# Print the first ten elements of each RDD generated in this DStream to the console
# Using pprint to reduce verbosity and keep a clean output
wordCounts.pprint()

# Start the computation
ssc.start()

# Wait for the computation to terminate
ssc.awaitTermination()
