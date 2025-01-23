```markdown
# WebSocket API for Flag Pattern Detection in EUR/USD Chart (MetaTrader5)

This project is a WebSocket-based API built using Django and Django Channels. The API detects flag patterns in EUR/USD price data retrieved from MetaTrader5 (MT5) and provides real-time updates via WebSocket.

The goal is to detect professional-grade flag patterns in the EUR/USD currency pair and notify clients with flag pattern details when detected.

## Features
- **WebSocket API**: Real-time communication between server and client for flag pattern detection.
- **MetaTrader5 Integration**: Fetches EUR/USD price data using MetaTrader5's API.
- **Pattern Detection**: Uses flagpole, consolidation, and breakout methods to detect flag patterns.
- **Django + Channels**: The WebSocket API is built using Django and Django Channels for asynchronous communication.

## Project Setup

### Prerequisites
- Python 3.12 or above
- MetaTrader5 (MT5) client installed and running
- Django 5.0 or above
- MetaTrader5 Python API (`MetaTrader5` package)
- Redis (optional for real-time message queue)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/flag-pattern-detection.git
   cd flag-pattern-detection
   ```

2. **Set up a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/MacOS
   venv\Scripts\activate     # For Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file**:

   Create a `.env` file in the root directory of your project with the following contents:

   ```plaintext
   DJANGO_SECRET_KEY=
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   PYTHONUNBUFFERED=1

   MT5_ACCOUNT=
   MT5_PASSWORD=
   MT5_SERVER=
   MT5_INVESTOR_PASSWORD=
   USERNAME=mojtaba
   USER_UID=1000
   USER_GID=1000
   DJANGO_SETTINGS_MODULE=config.settings
   ```

   - Replace `MT5_ACCOUNT`, `MT5_PASSWORD`, `MT5_SERVER`, and other sensitive information with your actual MetaTrader5 account details.
   - Ensure that the `DJANGO_SECRET_KEY` is kept secret in production.

5. **Migrate the database:**

   ```bash
   python manage.py migrate
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

   The WebSocket server will be accessible at `ws://127.0.0.1:8000/ws/test/`.

## Usage

### WebSocket API

- The WebSocket API listens for a connection from the client at the endpoint `/ws/test/`.
- Once the connection is established, the server continuously checks the EUR/USD price data from MetaTrader5.
- The flag pattern detection process runs every 60 seconds and sends updates to the client if a pattern is detected.
- If a flag pattern is detected, a JSON message with the details is sent back to the client.

#### WebSocket Message Structure

- **Incoming Message**: The WebSocket API expects no specific messages from the client.
- **Outgoing Message**:
  - If a flag pattern is detected, the following JSON structure is sent:
  
  ```json
  {
      "flag_detected": true,
      "details": {
          "time": "2025-01-23 10:10:00",
          "price": 1.2000,
          "details": {
              "flagpole_start_time": "2025-01-23 09:50:00",
              "flagpole_end_time": "2025-01-23 09:55:00",
              "consolidation_start_time": "2025-01-23 09:55:00",
              "consolidation_end_time": "2025-01-23 10:00:00",
              "breakout_start_time": "2025-01-23 10:05:00"
          }
      }
  }
  ```

  - If no flag pattern is detected, the message will look like:
  
  ```json
  {
      "flag_detected": false
  }
  ```

  - In case of an error, the error message is sent:
  
  ```json
  {
      "flag_detected": false,
      "error": "Error message describing the issue"
  }
  ```

### Example WebSocket Client

You can use any WebSocket client to connect to the API. Here's an example using JavaScript and the browser's native WebSocket API:

```javascript
const socket = new WebSocket('ws://127.0.0.1:8000/ws/test/');

socket.onopen = function(e) {
    console.log("Connection established");
};

socket.onmessage = function(event) {
    const message = JSON.parse(event.data);
    if (message.flag_detected) {
        console.log("Flag pattern detected:", message.details);
    } else {
        console.log("No flag pattern detected.");
    }
};

socket.onerror = function(error) {
    console.error("WebSocket Error:", error);
};

socket.onclose = function(event) {
    console.log("Connection closed");
};
```

### Error Handling
- If MetaTrader5 connection fails, or the data retrieval is unsuccessful, the system will send an error message with details about the issue.
  
## Code Structure

- **`consumers.py`**: Contains the WebSocket consumer that handles the flag pattern detection process.
- **`utils.py`**: Contains the logic for connecting to MetaTrader5, fetching EUR/USD data, and detecting flag patterns.
- **`settings.py`**: Configures Django settings, including WebSocket and environment variables.

## Testing

### Unit Tests

To run the unit tests:

1. **Install pytest and pytest-asyncio:**

   ```bash
   pip install pytest pytest-asyncio
   ```

2. **Run the tests:**

   ```bash
   pytest
   ```

### WebSocket Tests

The WebSocket API can be tested with `pytest` and `channels.testing.WebsocketCommunicator`. These tests simulate WebSocket connections and validate the functionality of the flag pattern detection.

## Docker

If you want to deploy the application using Docker, you can build and run the containers using the following commands:

1. **Build the Docker image:**

   ```bash
   docker-compose build
   ```

2. **Run the containers:**

   ```bash
   docker-compose up
   ```

This will spin up a Docker container running the Django app with the WebSocket API, and it will be accessible at `ws://127.0.0.1:8000/ws/test/`.

## Contributing

Feel free to open issues or submit pull requests for improvements, bug fixes, or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Key Updates:
1. **.env File**: Detailed `.env` configuration for your project, including MetaTrader5 account credentials and Django settings.
2. **Installation Instructions**: Updated with `.env` configuration and the necessary steps to run the project.
3. **Usage**: Clarified WebSocket message structure and example client.
4. **Testing**: Added instructions for unit testing and WebSocket tests.
5. **Docker**: Added detailed steps for deploying with Docker. 