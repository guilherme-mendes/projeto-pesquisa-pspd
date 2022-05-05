from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split
import pyspark.sql.functions as F

class SparkKafka:

    def __init__(self):
        self.topic = "word-topic"
        self.broker = "localhost:9092"
        self.spark_master = "localhost:7077"

        self.spark = SparkSession \
                    .builder \
                    .appName("StructuredNetworkWordCount") \
                    .getOrCreate()

        self.spark.sparkContext.setLogLevel("ERROR")

    def _count_words_by_substr(self, df, substring):
        grouped_words = df.filter(F.lower(F.col("word").substr(1, 1)) == substring).groupBy().count()
        return grouped_words.selectExpr("cast (count as string) %s" % substring)

    def _count_words_by_length(self, df, length, numeral):
        grouped_words = df.filter(F.length("word") == length).groupBy().count()
        return grouped_words.selectExpr(f"cast (count as string) {numeral}")

if __name__ == "__main__":
    sprk = SparkKafka()
    spark_frame = sprk.spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", sprk.broker) \
        .option("subscribe", sprk.topic) \
        .option("port", 9999) \
        .load() \
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    words = spark_frame.select(
        explode(
            split(spark_frame.value, " ")
        ).alias("word")
    )


    word_counts = words.groupBy("word").count()
    every_word = words.groupBy().count()

    p_words = sprk._count_words_by_substr(words, "p")
    s_words = sprk._count_words_by_substr(words, "s")
    r_words = sprk._count_words_by_substr(words, "r")

    six_words = sprk._count_words_by_length(words, 6, "six")
    eight_words = sprk._count_words_by_length(words, 8, "eight")
    eleven_words = sprk._count_words_by_length(words, 11, "eleven")

    query_counts = word_counts\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .start()

    query_every_word = every_word\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .start()

    query_p = p_words\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()

    query_s = s_words\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()

    query_r = r_words\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()

    query_6 = six_words\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()
    
    query_8 = eight_words\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()
    
    query_11 = eleven_words\
        .writeStream\
        .outputMode("update")\
        .format("console")\
        .start()

    sprk.spark.streams.awaitAnyTermination()
