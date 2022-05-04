from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext


def updateFunc(value, sum_last):
    return sum(value) + (sum_last or 0)

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
ssc = StreamingContext(sc, 5)
ssc.checkpoint("hdfs://hadoop:9000/checkpoint")

state_rdd = sc.emptyRDD()

# Adicionando a fila rdd a um DStream
msg = ssc.socketTextStream("server", 9999)

# Fazer a contagem de palavras
word = msg.flatMap(lambda line: line.split(" ")).filter(lambda word: word != "")
word_count = word.map(lambda word: (word.lower(), 1)).reduceByKey(lambda x, y: x + y)

oper = word_count.updateStateByKey(updateFunc, initialRDD=state_rdd)
# Use transform() para acessar quaisquer transformações rdd não disponíveis diretamente na SparkStreaming
sort = oper.transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending=False))
word_len = oper.reduce(lambda x, y: ("Numero total de palavras", x[1] + y[1]))
sort.pprint()

word_len.pprint()

ssc.start()  # Iniciar o streaming
ssc.awaitTermination()  # Aguarde que o streaming termine
