# 1. Use a lightweight official Python image as the foundation
FROM python:3.11-slim

# 2. Set the operational workspace directory inside the container image
WORKDIR /app

# 3. Install necessary operating system utilities for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy over the dependency list checklist first to leverage Docker caching layers
COPY requirements.txt .

# 5. Build and install all libraries globally inside the container environment
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the entire local project directory assets inside the working framework
COPY . .

# 7. Expose ports 8000 (FastAPI Backend) and 8501 (Streamlit Frontend Dashboard)
EXPOSE 8000
EXPOSE 8501

# 8. Set up a simple shell environment script trigger to spin up both systems simultaneously
CMD uvicorn src.app:app --host 0.0.0.0 --port 8000 & streamlit run dashboard/UI.py --server.port 8501 --server.address 0.0.0.0
