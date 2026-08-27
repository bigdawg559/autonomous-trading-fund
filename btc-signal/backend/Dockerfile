FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY btc_signal ./btc_signal
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "btc_signal.worker"]
