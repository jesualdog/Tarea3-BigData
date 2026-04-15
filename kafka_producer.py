import json
import random
import time
from kafka import KafkaProducer

def generate_sale():
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Beauty", "Sports"]
    return {
        "transaction_id": random.randint(10000, 99999),
        "product_category": random.choice(categories),
        "quantity": random.randint(1, 5),
        "amount": round(random.uniform(10.0, 500.0), 2),
        "timestamp": int(time.time())
    }

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("Iniciando generador de ventas en tiempo real...")
while True:
    sale = generate_sale()
    producer.send("sensor_data", value=sale)   # Usamos el mismo topic del Anexo 3
    print(f"Venta enviada: {sale}")
    time.sleep(1)  # una venta por segundo (puedes cambiarlo)
