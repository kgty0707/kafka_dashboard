import sqlite3
from kafka import KafkaConsumer
import json
import time
from river import linear_model, preprocessing, metrics

# Kafka 설정
KAFKA_TOPIC = "test-topic"
KAFKA_SERVER = "localhost:9092"
DB_PATH = "example.db"

# SQLite 데이터베이스 초기화
def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kafka_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 자동 증가 ID
            room_temp REAL,                       -- 방온도
            hand_temp REAL,                       -- 손온도
            min_temp REAL,                        -- 최저온도
            max_temp REAL,                        -- 최고온도
            prev_temp REAL,                       -- 이전 온도
            curr_temp REAL,                       -- 현재 온도
            adjective TEXT                        -- 열감 인지 형용사
        )
    """)
    conn.commit()
    conn.close()


def save_to_db(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kafka_data (room_temp, hand_temp, min_temp, max_temp, prev_temp, curr_temp, adjective)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["room_temp"],
        data["hand_temp"],
        data["min_temp"],
        data["max_temp"],
        data["prev_temp"],
        data["curr_temp"],
        data["adjective"]
    ))
    conn.commit()
    conn.close()


def train_streaming_model(consumer):
    scaler = preprocessing.StandardScaler()
    model = linear_model.LogisticRegression()  # Adjective 예측을 위한 분류 모델
    metric = metrics.Accuracy()  # 분류 모델의 정확도 평가

    total_count = 0
    start_time = time.time()

    print(f"Listening to topic: {KAFKA_TOPIC} on {KAFKA_SERVER}")

    for message in consumer:
        data = message.value

        # 데이터베이스에 저장
        save_to_db(data)

        # 모델 학습
        try:
            # 독립 변수와 종속 변수 설정
            X = {
                "room_temp": data["room_temp"],
                "hand_temp": data["hand_temp"],
                "min_temp": data["min_temp"],
                "max_temp": data["max_temp"],
                "prev_temp": data["prev_temp"],
                "curr_temp": data["curr_temp"],
            }
            y = data.get("adjective")  # 종속 변수: 열감 인지 형용사

            if y is None:
                print(f"Skipping invalid data: {data}")
                continue

            # 스케일링 및 모델 학습
            scaler.learn_one(X)  # 상태 업데이트
            X = scaler.transform_one(X)  # 변환된 데이터
            y_pred = model.predict_one(X)  # 예측 값

            if y_pred is None:
                print(f"Skipping due to invalid prediction: {y_pred}")
                continue

            model.learn_one(X, y)  # 모델 업데이트

            # 평가 지표 업데이트
            metric.update(y, y_pred)  # 평가 지표 업데이트
            print(f"Trained on: {data}, Predicted: {y_pred}, Actual: {y}, Metric: {metric.get():.2f}")

        except KeyError as e:
            print(f"Invalid data format: {e}")

        total_count += 1

        # 주기적인 통계 출력
        if total_count % 100 == 0:  # 100개마다 통계 출력
            elapsed_time = time.time() - start_time
            tps = total_count / elapsed_time if elapsed_time > 0 else 0
            print(f"=====================================================")
            print(f"총 처리 시간:  {elapsed_time:.2f} 초")
            print(f"총 처리 건수:  {total_count}")
            print(f"초당 처리 건수:  {tps:.2f}")
            print(f"모델 평가 지표 (Accuracy): {metric.get():.2f}")
            print(f"=====================================================")


def consume_data():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset='earliest'
    )
    train_streaming_model(consumer)


def consume_metrics():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset='earliest'
    )
    for message in consumer:
        yield message.value

# if __name__ == "__main__":
#     create_table()
#     consume_data()