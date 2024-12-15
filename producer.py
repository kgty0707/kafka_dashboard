import json
import time
import random
from kafka import KafkaProducer
import streamlit as st

# Kafka 설정
KAFKA_TOPIC = "test-topic"
KAFKA_SERVER = "localhost:9092"

# Producer 생성
producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# 데이터 전송 함수
def send_data(interval=4, num_messages=500):
    """
    Kafka 토픽으로 데이터를 전송.
    :param interval: 메시지 전송 간격 (초)
    :param num_messages: 전송할 메시지 개수
    """
    for _ in range(num_messages):
        data = generate_data()
        producer.send(KAFKA_TOPIC, value=data)  # Kafka 토픽으로 전송
        print(f"Sent: {data}")
        time.sleep(interval)
    producer.flush()  # 전송 대기 중인 메시지 모두 전송


def generate_data():
    adjectives = ["Cold", "Cool", "Neutral", "Warm", "Hot"]

    room_temp = round(random.uniform(15, 30), 2)  # 방온도 (15~30도)
    hand_temp = round(random.uniform(20, 35), 2)  # 손온도 (20~35도)
    min_temp = round(min(room_temp, hand_temp) - random.uniform(1, 3), 2)  # 최저온도
    max_temp = round(max(room_temp, hand_temp) + random.uniform(1, 3), 2)  # 최고온도
    prev_temp = round(random.uniform(10, 40), 2)  # 이전 온도
    curr_temp = round((prev_temp + random.uniform(-5, 5)), 2)  # 현재 온도
    adjective = random.choice(adjectives)  # 열감 인지 형용사
    return {
        "room_temp": room_temp,
        "hand_temp": hand_temp,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "prev_temp": prev_temp,
        "curr_temp": curr_temp,
        "adjective": adjective
        }

if __name__ == "__main__":
    send_data(interval=0.5, num_messages=500)