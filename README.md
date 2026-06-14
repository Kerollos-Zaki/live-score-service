# Live Score Service

An event-driven, full-stack application designed to stream and display real-time sports match scores[cite: 1]. The system uses a decoupled producer-consumer architecture to handle real-time data flow efficiently, rendering live updates instantly on a modern frontend dashboard[cite: 1].

## 🛠️ Tech Stack

### Backend & Event Streaming
* **Python**: Core backend application logic[cite: 1].
* **Producer / Consumer Architecture**: Decoupled messaging scripts (`producer.py` & `consumer.py`) built to handle live, high-frequency score data streaming[cite: 1].

### Frontend Dashboard
* **React**: Component-based UI for displaying real-time match data dynamically[cite: 1].
* **Vite**: A fast, modern build tool and development server for the frontend framework[cite: 1].

### Infrastructure & Operations
* **Docker / Docker Compose**: Multi-container dockerization ensuring seamless environment setup for the message brokers, backend services, and client dashboard[cite: 1].
