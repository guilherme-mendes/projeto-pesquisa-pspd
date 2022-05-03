from pyspark.sql import SparkSession




# class SparkKafka:

#     def __init__(self):
#         self.topic = "word-topic"
#         self.broker = "kafka1://localhost:9091"
#         self.spark_master = "spark://dutra:7077"

#         self.spark = SparkSession \
#                     .builder \
#                     .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1') \
#                     .master(self.spark_master) \
#                     .appName("StructuredNetworkWordCount") \
#                     .getOrCreate()

#         self.spark.sparkContext.setLogLevel('WARN')



# if __name__ == '__main__':
#     spark_kafka = SparkKafka()
#     stream = spark_kafka.spark \
#         .readStream \
#         .format("kafka") \
#         .option("kafka.bootstrap.servers", spark_kafka.broker) \
#         .option("subscribe", spark_kafka.topic) \
#         .option('startingOffsets', 'latest') \
#         .option('includeTimestamp', 'true') \
#         .load()

#     stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

#     stream.writeStream \
#         .outputMode("complete") \
#         .format("console") \
#         .outputMode("append") \
#         .option('truncate', 'false') \
#         .start()
        
    # stream.awaitTermination()

if __name__ == "__main__":

    spark = SparkSession.builder.appName("StructuredNetworkWordCount").config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1').getOrCreate()
    spark.sparkContext.setLogLevel('DEBUG')

    df = spark\
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka1://localhost:9091") \
        .option("subscribe", "word-topic") \
        .option('startingOffsets', 'latest') \
        .option('includeTimestamp', 'true') \
        .load()

    df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    lines = df.select("value")
    count_words = lines.count()

    print(df)
    print(lines)
    print(count_words)

    find = count_words.writeStream \
           .outputMode("complete") \
           .format("console") \
           .outputMode("append") \
           .option('truncate', 'false') \
           .start()

    find.awaitTermination()
