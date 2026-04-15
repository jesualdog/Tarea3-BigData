from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum as spark_sum, count
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, TimestampType

spark = SparkSession.builder \
    .appName("RealTimeRetailSalesStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("transaction_id", IntegerType()),
    StructField("product_category", StringType()),
    StructField("quantity", IntegerType()),
    StructField("amount", FloatType()),
    StructField("timestamp", TimestampType())
])

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sensor_data") \
    .load()

parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Análisis en tiempo real: ventas por ventana de 1 minuto
windowed_sales = parsed_df \
    .groupBy(window(col("timestamp"), "1 minute"), "product_category") \
    .agg(
        spark_sum("amount").alias("ventas_totales"),
        count("*").alias("transacciones")
    )

query = windowed_sales \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
