---


## Real-Time Kafka Producer and Consumer with Streamlit Dashboard

This project demonstrates a **Kafka Producer** for sending data and a **Streamlit Dashboard** for consuming, processing, and visualizing real-time data. The system uses River for online machine learning and processes metrics such as **MAE** (Mean Absolute Error) and **Loss** values in real time.

---

## **Project Overview**

1. **Kafka Producer**:
   - Simulates sensor data and sends it to a Kafka topic (`test-topic`).
   - Data format includes:
     - `room_temp`: Room temperature.
     - `hand_temp`: Hand temperature.
     - `min_temp`: Minimum temperature.
     - `max_temp`: Maximum temperature.
     - `prev_temp`: Previous temperature.
     - `curr_temp`: Current temperature.
     - `adjective`: Sensory perception (e.g., "Cold", "Neutral", "Warm", etc.).

2. **Streamlit Dashboard**:
   - Consumes data from Kafka.
   - Trains a **linear regression model** using River for online learning.
   - Calculates and visualizes metrics such as:
     - **Mean Absolute Error (MAE)**
     - **Loss** (Squared loss function)
   - Displays real-time charts for:
     - MAE and Loss values.
     - TPS (Transactions per Second) and Processing Time.

---

## **Kafka and Zookeeper Setup**

For Kafka and Zookeeper installation, refer to the detailed guide provided in the following **Notion Page**(written in korean):

📘 **[Kafka and Zookeeper Installation Guide](https://alluring-walnut-362.notion.site/Kafka-15778b1f0c1080ed89cec6bc5e5ae4b2?pvs=4)**

This guide includes:
- Installing Apache Kafka and Zookeeper on Windows/Linux.
- Configuring `server.properties` and `zookeeper.properties`.
- Starting Zookeeper and Kafka services.
- Creating and managing Kafka topics.

---

## **Features**

- **Kafka Producer**:
  - Generates mock temperature data.
  - Sends data to a Kafka topic (`test-topic`) in real time.

- **Real-Time Streamlit Dashboard**:
  - Visualizes real-time metrics:
    - **MAE** and **Loss** in a line chart.
    - **Transactions per Second (TPS)** and **Processing Time** in another chart.
  - Updates dynamically as new data arrives.

- **Online Machine Learning**:
  - Uses the **River** library for real-time model training.
  - Processes streaming data efficiently.

---

## **Data Format**

Each Kafka message is structured as follows:

```json
{
  "room_temp": 23.56,
  "hand_temp": 28.12,
  "min_temp": 20.32,
  "max_temp": 30.45,
  "prev_temp": 25.14,
  "curr_temp": 26.45,
  "adjective": "Warm"
}
```

---

## **Tech Stack**

- **Backend**: Kafka, Python (Kafka Producer & Consumer)
- **Frontend**: Streamlit (Dashboard)
- **Machine Learning**: River (Online Learning Library)
- **Data Storage**: SQLite (Optional)

---

## **Project Setup**

Follow these steps to set up and run the project:

### **1. Prerequisites**

- Python (>= 3.12)
- Kafka (Install Apache Kafka and Zookeeper)
- Git

### **2. Install Dependencies**

Clone the repository and install required libraries:

```bash
git clone https://github.com/your-username/kafka-streamlit-dashboard.git
cd kafka-streamlit-dashboard
pip install -r requirements.txt
```

### **3. Start Kafka and Zookeeper**

Ensure Kafka and Zookeeper are running on your machine. Follow the installation guide:  
📘 **[Kafka and Zookeeper Installation Guide](https://alluring-walnut-362.notion.site/Kafka-15778b1f0c1080ed89cec6bc5e5ae4b2?pvs=4)**

```bash
# Start Zookeeper
.\bin\windows\zookeeper-server-start.bat config\zookeeper.properties

# Start Kafka Server
.\bin\windows\kafka-server-start.bat config\server.properties
```

### **4. Create a Kafka Topic**

Create a topic named `test-topic`:

```bash
.\bin\windows\kafka-topics.bat --create --topic test-topic --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

### **5. Run Kafka Producer**

Start the Kafka producer to send mock data:

```bash
python producer.py
```

### **6. Start Streamlit Dashboard**

Launch the Streamlit Dashboard to visualize the metrics:

```bash
streamlit run app.py
```

---

## **File Structure**

```plaintext
kafka-streamlit-dashboard/
│
├── producer.py            # Kafka producer script for sending mock data
├── consumer.py            # Kafka consumer script with real-time training
├── app.py                 # Streamlit Dashboard for visualization
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

---

## **Visualization**
![image](https://github.com/user-attachments/assets/a62b7b61-445f-49ef-9102-8b43d2b2119d)

The Streamlit Dashboard consists of the following charts:

1. **Real-Time MAE and Loss**:
   - Line chart showing model performance over time.

2. **Real-Time TPS and Processing Time**:
   - Line chart showing system throughput and latency.

---

## **Dependencies**

Install the following libraries:

```plaintext
streamlit
kafka-python
plotly
pandas
river
```

---

## **Contact**

For questions, please contact:

- **Name**: Park heymin
- **Email**: phm0707@hanyang.ac.kr

```
