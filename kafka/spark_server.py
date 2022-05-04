from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark import SparkConf
import pyspark.sql.functions as F

class SparkKafka:

    def __init__(self):
        self.topic = "word-topic"
        self.broker = "localhost:9092"
        self.spark_master = "spark://localhost:7077"

        self.spark = SparkSession \
                    .builder \
                    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.1') \
                    .master(self.spark_master) \
                    .appName("StructuredNetworkWordCount") \
                    .getOrCreate()

        self.spark.sparkContext.setLogLevel('WARN')

if __name__ == '__main__':
    sprk = SparkKafka()
    spark_frame = sprk.spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", sprk.broker) \
        .option("subscribe", sprk.topic) \
        .load() \
        .selectExpr("CAST(value AS STRING)")

    words = spark_frame.select(
        # explode transforma cada item do array em uma linha
        explode(
            split(spark_frame.value, ' ')
        ).alias('word')
    )


    word_counts = words.groupBy('word').count()
    every_word = words.groupBy().count()

    query = word_counts\
        .writeStream\
        .outputMode('complete')\
        .format('console')\
        .start()

    query.awaitTermination()