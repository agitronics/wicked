
This project is a comprehensive network scanning and vulnerability assessment tool that combines various scanning techniques and provides a user-friendly interface for managing scans and reports.

## Features

- Advanced target acquisition
- Multiple scanning modules (TruffleHog, tcpdump, TheDigger, Quimera, etc.)
- Real-time scan progress updates
- Report generation and management
- Customizable scan options
- Import target IP lists
- Save and load scan settings

## Prerequisites

- Python 3.8+
- Node.js 14+
- Redis server

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/agitronics/wicked.git
   cd advanced-network-tools
   ```

2. Set up the Python virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

## Running the Application

1. Start the Redis server:
   ```
   redis-server
   ```

2. Start the Celery worker:
   ```
   celery -A app.celery worker --loglevel=info
   ```

3. Start the Flask backend:
   ```
   python app.py
   ```

4. In a new terminal, start the Next.js frontend:
   ```
   cd frontend
   npm run dev
   ```

5. Access the application at `http://localhost:3000`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational and ethical testing purposes only. Do not use it on networks or systems you do not own or have explicit permission to test. The authors are not responsible for any misuse or damage caused by this tool.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
