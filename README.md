
# Live Score Service

This project is a full-stack application designed to process and display live scores. The application features a Python-based backend architecture and a modern React frontend.

## 🛠️ Tech Stack

* **Backend Environment**: The backend is built using Python, utilizing a `requirements.txt` file for dependencies and `main.py` as a primary script.


* **Message Processing**: The architecture utilizes a streaming or messaging model, indicated by the dedicated `producer.py` and `consumer.py` scripts.


* **Frontend Framework**: The client side is a React application (`App.jsx`, `main.jsx`) bundled using Vite (`vite.config.js`).


* **Package Management**: The frontend relies on Node.js, using `package.json` and `package-lock.json`.


* **Infrastructure**: The service includes a `docker-compose.yml` file, indicating it is containerized for streamlined deployment.



## ⚽ Featured Teams

Based on the frontend assets, the service includes dedicated logos and graphics for the following football clubs:

* Al Ahly (`ahly.png`)


* Zamalek (`zamalek.png`)


* Liverpool (`Liverpool.png`)


* Manchester United (`Man United.png`)



## 📁 Project Structure

* `main.py` - Core backend application file.


* `producer.py` - Script responsible for producing or emitting live score data.


* `consumer.py` - Script responsible for consuming the score data.


* `docker-compose.yml` - Docker configuration for running the application environment.


* `requirements.txt` - Python backend dependencies.


* `frontend/` - Root directory for the client-side UI.


* `src/` - Contains the core React components (`App.jsx`, `main.jsx`) and stylesheets (`App.css`, `index.css`).


* `public/assets/` - Contains static images and team logos.


* `vite.config.js` - Configuration for the Vite build tool.


* `eslint.config.js` - Linting configuration for frontend code quality.
