# TODO 1: Pilih base image Python resmi yang ringan.
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

# TODO 2: Install dependency dari requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# TODO 3: Jalankan simulator saat container start.
CMD ["python3", "src/order_simulator.py"]