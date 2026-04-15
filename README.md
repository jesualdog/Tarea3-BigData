# Tarea3 - BigData
Diseñar e implementar soluciones de almacenamiento y procesamiento de grandes volúmenes de datos utilizando herramientas como **Hadoop, Spark y Kafka**, para desarrollar infraestructuras tecnológicas que soporten el análisis eficiente de datos.

## Tarea 3 - Procesamiento de Datos con Apache Spark y Kafka
**Curso:** Big Data  
**Código:** 202016911  
**Elaborado por:** Jesualdo Gutiérrez  
**Universidad Nacional Abierta y Distancia (UNAD)**

## Descripción del Proyecto
Este proyecto implementa un sistema completo de análisis de **ventas en tiempo real** y procesamiento histórico utilizando:

- **Apache Spark** para procesamiento en batch (análisis histórico del dataset de ventas).
- **Apache Kafka + Spark Streaming** para procesamiento en tiempo real (simulación de ventas continuas).

El objetivo es demostrar el uso combinado de batch + streaming, cumpliendo con el Resultado de Aprendizaje 2 de la asignatura.

## Tecnologías Utilizadas
- Apache Spark 3.5.3
- Apache Kafka 3.9.2
- Python 3
- Kafka-Python
- Máquina Virtual Ubuntu con Hadoop y Spark

## Estructura del Proyecto

<img width="600" height="250" alt="image" src="https://github.com/user-attachments/assets/d16b6eba-9734-447e-ab7b-43c7c0cce2f4" />

## Requisitos Previos
- Máquina virtual configurada con Hadoop y Spark (usuario: `vboxuser` / pass: `bigdata`)
- Kafka y ZooKeeper ejecutándose
- Dataset `retail_sales_dataset.csv` copiado en `/home/vboxuser/`

**Pasos para descargar dataset**
- En tu PC (navegador):  
Ve a: https://www.kaggle.com/datasets/mohammadtalib786/retail-sales-dataset  
Inicia sesión en tu cuenta de Kaggle.  
Haz clic en el botón Download (se descargará retail_sales_dataset.csv).

## Instrucciones de Ejecución

### 1. Implementación en Spark (Ventas)

Procesamiento en batch (código completo)  
Crea el archivo `batch_retail_sales.py` en la VM con nano
```
nano batch_retail_sales.py
```
### 2. Procesamiento en Batch (Spark)
```
spark-submit batch_retail_sales.py
```
**Qué hace:**
Carga el dataset histórico, limpia los datos, calcula ventas totales por categoría, ventas por hora y por ventana diaria.
Guarda los resultados en las carpetas `output_batch_sales/` y `output_batch_windowed/`.

### 3. Procesamiento en Tiempo Real (Kafka + Spark Streaming)
Iniciar ZooKeeper y Kafka (si no están corriendo)
```
sudo /opt/Kafka/bin/zookeeper-server-start.sh /opt/Kafka/config/zookeeper.properties &   
sudo /opt/Kafka/bin/kafka-server-start.sh /opt/Kafka/config/server.properties &
```
### 4. Creamos un tema (topic) de Kafka
```
/opt/Kafka/bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic sensor_data
```
**Nota:** El Topic quedó con el nombre `sensor_data` pero puedes colocar cualquier otro nombre, acorde a tu proyecto.

### 5. Implementación del productor(producer) de Kafka
Creamos un archivo llamado kafka_producer.py
```
nano kafka_producer.py
```
Este archivo contiene un script que genera datos simulados de ventas y los envía al tema (topic) de Kafka que creamos anteriormente.

### 6. Implementación del consumidor con Spark Streaming
Crearemos un consumidor(consumer) utilizando Spark Streaming para procesar los datos en tiempo real. Crea un archivo llamado spark_streaming_consumer.py
```
nano spark_streaming_consumer.py
```
Este archivo contiene un script que utiliza Spark Streaming para leer datos del tema(topic) de Kafka, procesa los datos en ventanas de tiempo de 1 minuto y calcula las ventas totales por categoría de producto y cantidad de transacciones

### 7. Ejecución y análisis
Ejecutar el Productor (en una terminal)
```
python3 kafka_producer.py
```
Ejecutar el Consumidor Spark Streaming (en otra terminal)
```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 spark_streaming_consumer.py
```
**Nota:** es importante primero ejecutar el script de productor y luego el del consumidor

### 8. Spark Web UI (Monitoreo)
Mientras cualquiera de los jobs esté corriendo, en este caso se accede a: `http://192.168.1.8:4040`

## Resultados Esperados

- **Batch:** Estadísticas de ventas totales por categoría, por hora y por ventana de tiempo.  
- **Streaming:** Ventas totales y cantidad de transacciones actualizadas cada minuto por categoría de producto (Electronics, Clothing, Beauty, etc.).
