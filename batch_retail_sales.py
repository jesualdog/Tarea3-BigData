from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, sum as spark_sum, count, desc, window

spark = SparkSession.builder \
    .appName("BatchRetailSalesAnalysis") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Cargar el dataset (nombre exacto del archivo que tienes)
df = spark.read.csv("retail_sales_dataset.csv", header=True, inferSchema=True)

# Convertir fecha (formato exacto de tu CSV)
df = df.withColumn("timestamp", to_timestamp(col("Date"), "yyyy-MM-dd"))

print("=== ESQUEMA DEL DATASET ===")
df.printSchema()

print("=== ESTADÍSTICAS BÁSICAS ===")
df.describe().show()

# Limpieza (por si hay valores nulos o negativos)
df_clean = df.filter((col("Total Amount") > 0) & col("Total Amount").isNotNull())

print("=== ANÁLISIS EXPLORATORIO (EDA) ===")
# 1. Ventas totales por categoría de producto
df_clean.groupBy("Product Category").agg(
    spark_sum("Total Amount").alias("Ventas_Totales"),
    count("*").alias("Cantidad_Transacciones")
).orderBy(desc("Ventas_Totales")).show()

# 2. Ventas por ventana de 1 día (similar al streaming)
windowed_sales = df_clean.groupBy(
    window(col("timestamp"), "1 day"), "Product Category"
).agg(
    spark_sum("Total Amount").alias("Ventas_Totales"),
    count("*").alias("Transacciones")
).orderBy("window")
windowed_sales.show(truncate=False)

# Guardar resultados para que puedas revisarlos
df_clean.write.mode("overwrite").csv("output_batch_sales", header=True)
windowed_sales.write.mode("overwrite").csv("output_batch_windowed", header=True)

print("\n¡PROCESAMIENTO BATCH FINALIZADO!")
print("Resultados guardados en: output_batch_sales/ y output_batch_windowed/")
spark.stop()
