# Disaster-AI Web App

### Overview:
Disaster-AI is a web application that provides real-time, relevant responses to user queries during disasters using a Retrieval-Augmented Generation (RAG) model. The app allows users to ask disaster-related questions and receive accurate information instantly. Key features include:

- **Text-based query input**: Users can type questions about disaster relief, safety tips, or other calamity-related concerns.
- **Real-time responses**: The system fetches relevant content using a large language model (T5-large).
- **Web-based platform**: Accessible on any browser with a clean, easy-to-use interface.
- **Potential offline functionality** (future update).

---

### Features:
- **Quick Help via Text Box**: Users input questions in a text box and receive instant responses.
- **Calamity-Specific Information**: Users can ask questions on various aspects of a disaster, from preparedness to recovery.
- **Real-time, Accurate Responses**: The app utilizes a RAG-based approach to ensure responses are relevant and timely.

---

### Prerequisites:
Before running the project, ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v14 or above)
- [MongoDB](https://www.mongodb.com/) (for local database, or use a cloud-based MongoDB service like Atlas)
- [npm](https://www.npmjs.com/) (comes with Node.js)

---

### Installation Instructions:

1. **Clone the repository**:
   ```bash
   git clone <repo-link>
   cd <repo-directory>
   ```

2. **Install dependencies**:

   In the root directory (for the backend):
   ```bash
   npm install
   ```

   Navigate to the `client` folder (for the frontend):
   ```bash
   cd client
   npm install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory and add your configuration details (API keys, database connection strings, etc.). Example:
   ```
   MONGO_URI=your-mongodb-uri
   PORT=5000
   REACT_APP_API_URL=http://localhost:5000
   ```

4. **Run the app**:
   First, start the server (back-end):
   ```bash
   npm start
   ```

   Then, in another terminal, start the front-end (React):
   ```bash
   cd client
   npm start
   ```

   The app will be available on `http://localhost:3000`.

---

### How to Use:
1. Open your browser and navigate to `http://localhost:3000`.
2. Type a disaster-related query in the provided text box.
3. Hit submit to get real-time responses related to your question.

---

### Contributing:
Feel free to contribute by submitting issues or pull requests. Any feedback or suggestions to improve the app are welcome!

---
