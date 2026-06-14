# Live Score Service

An event-driven, full-stack application designed to stream and display real-time sports match scores. The system uses a decoupled producer-consumer architecture to handle real-time data flow efficiently, rendering live updates instantly on a modern frontend dashboard.

## 🛠️ Tech Stack

<p align="left">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" height="40" alt="Python" title="Python" /> &nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg" height="40" alt="React" title="React" /> &nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vitejs/vitejs-original.svg" height="40" alt="Vite" title="Vite" /> &nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg" height="40" alt="Docker" title="Docker" />
</p>

### Backend & Event Streaming
* **Python**: Core backend application logic.
* **Producer / Consumer Architecture**: Decoupled messaging scripts (`producer.py` & `consumer.py`) built to handle live, high-frequency score data streaming.

### Frontend Dashboard
* **React**: Component-based UI for displaying real-time match data dynamically.
* **Vite**: A fast, modern build tool and development server for the frontend framework.

### Infrastructure & Operations
* **Docker / Docker Compose**: Multi-container dockerization ensuring seamless environment setup for the message brokers, backend services, and client dashboard.
