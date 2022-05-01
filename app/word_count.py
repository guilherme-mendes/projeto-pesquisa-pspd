from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext


conf = (
    SparkConf()
    .setMaster("spark://spark:7077")
    .setAppName("NetworkWordCount")
    .set("spark.dynamicAllocation.enabled", "false")
    .set("spark.shuffle.service.enabled", "false")
    .set("spark.streaming.driver.writeAheadLog.closeFileAfterWrite", "true")
    .set("spark.streaming.receiver.writeAheadLog.closeFileAfterWrite", "true")
    .set("spark.executor.memory", "512m")
    .set("spark.executor.instances", "2")
)

sc = SparkContext(conf=conf)

# Criar um StreamingContext com intervalo de lote de 5 segundos
ssc = StreamingContext(sc, 1)
ssc.checkpoint("hdfs://hadoop:9000/checkpoint")

rdd_state = sc.emptyRDD()


def functionUpd(value, sum_last):
    return sum(value) + (sum_last or 0)


# Adicionando a fila rdd a um DStream
lines = ssc.socketTextStream("server", 9999)

# Fazer a contagem de palavras
words = lines.flatMap(lambda line: line.split(" ")).filter(lambda word: word != "")
pairs = words.map(lambda word: (word.lower(), 1))
wordCounts = pairs.reduceByKey(lambda x, y: x + y)

running = wordCounts.updateStateByKey(functionUpd, initialRDD=rdd_state)

# Use transform() para acessar quaisquer transformações rdd não disponíveis diretamente na SparkStreaming
sorted = running.transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending=False))
wordsLen = running.reduce(lambda x, y: ("Numero total de palavras", x[1] + y[1]))
sorted.pprint()

wordsLen.pprint()

ssc.start()  # Iniciar o streaming
ssc.awaitTermination()  # Aguarde que o streaming termine
