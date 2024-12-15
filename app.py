import streamlit as st
import pandas as pd
import datetime
import time
from consumer import consume_metrics
from river import linear_model, preprocessing, metrics, optim
import plotly.express as px

# Streamlit 페이지 설정
st.set_page_config(page_title="Real-Time Model Metrics", layout="wide")
st.title("Real-Time Model Metrics Dashboard")

# Streamlit 차트 및 표시 초기화
placeholder = st.empty()  # MAE 차트를 위한 placeholder
placeholder_tps = st.empty()  # TPS 차트 및 Total Count를 위한 placeholder

# River 모델 초기화
scaler = preprocessing.StandardScaler()
model = linear_model.LinearRegression()
metric = metrics.MAE()
loss_fn = optim.losses.Squared()

# Kafka Consumer
metrics_stream = consume_metrics()

# 실시간 처리 루프
chart_data_mae = pd.DataFrame(columns=["Timestamp", "MAE", "Loss"])
chart_data_tps = pd.DataFrame(columns=["Timestamp", "TPS", "Processing Time (s)"])

# 처리 통계 초기화
total_count = 0
start_time = time.time()

adjective_mapping = {"Cold": 0, "Cool": 1, "Neutral": 2, "Warm": 3, "Hot": 4}

# 실시간 처리 루프
for data in metrics_stream:
    try:
        X = {k: data[k] for k in data if k not in ["adjective"]}
        y = adjective_mapping[data["adjective"]]  # 문자열을 숫자로 변환

        # 모델 학습 및 평가
        scaler.learn_one(X)
        X_scaled = scaler.transform_one(X)
        y_pred = model.predict_one(X_scaled)
        model.learn_one(X_scaled, y)
        metric.update(y, y_pred)

        # 처리 통계
        loss_value = loss_fn(y, y_pred)
        total_count += 1
        elapsed_time = time.time() - start_time
        tps = total_count / elapsed_time if elapsed_time > 0 else 0



        # 현재 MAE 추가
        current_time = datetime.datetime.now().strftime("%M:%S")
        new_data_mae = pd.DataFrame({
            "Timestamp": [current_time],  # x축 레이블 간결화
            "MAE": [metric.get()],
            "Loss": [loss_value]
        })
        new_data_tps = pd.DataFrame({
            "Timestamp": [current_time],
            "TPS": [tps],
            "Processing Time (s)": [elapsed_time]
        })

        # 데이터프레임 병합
        if chart_data_mae.empty:
            chart_data_mae = new_data_mae
        else:
            chart_data_mae = pd.concat([chart_data_mae, new_data_mae], ignore_index=True)

        if chart_data_tps.empty:
            chart_data_tps = new_data_tps
        else:
            chart_data_tps = pd.concat([chart_data_tps, new_data_tps], ignore_index=True)

        # 실시간 차트 업데이트: MAE
        fig_mae = px.line(
            chart_data_mae, 
            x="Timestamp", 
            y=["MAE", "Loss"], 
            title="Real-Time MAE and Loss",
            labels={"Timestamp": "Time (Minutes:Second)", "value": "Metrics"}
        )
        fig_mae.update_layout(xaxis_tickformat="%M:%S", xaxis_title="Time (Minutes:Second)", yaxis_title="Metrics")

        # 실시간 차트 업데이트: TPS & Processing Time
        fig_tps = px.line(
            chart_data_tps, 
            x="Timestamp", 
            y=["TPS", "Processing Time (s)"], 
            title="Real-Time TPS and Processing Time",
            labels={"Timestamp": "Time (Minutes:Second)", "value": "Metric"},
            line_shape="linear"
        )

        # 각 선의 색상 설정
        fig_tps.update_traces(
            line=dict(color="pink"),  # TPS 선 색상
            selector=dict(name="TPS")
        )
        fig_tps.update_traces(
            line=dict(color="red"),  # Processing Time 선 색상
            selector=dict(name="Processing Time (s)")
        )

        fig_tps.update_layout(
            xaxis_tickformat="%M:%S", 
            xaxis_title="Time (Minutes:Second)", 
            yaxis_title="Metrics"
        )

        # Streamlit 업데이트
        with placeholder.container():
            st.plotly_chart(fig_mae, use_container_width=True)
            col1, col2 = st.columns(2)
            col1.metric("Current MAE", f"{metric.get():.2f}")
            col2.metric("Current Loss", f"{loss_value:.2f}")

        with placeholder_tps.container():
            st.plotly_chart(fig_tps, use_container_width=True)
            st.metric("Total Processed", total_count)

    except KeyError as e:
        st.error(f"Invalid data format: {e}")
