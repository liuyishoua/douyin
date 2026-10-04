FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*
COPY requirements-web.txt .
RUN pip install --no-cache-dir -r requirements-web.txt
COPY . .
ENV PYTHONUNBUFFERED=1
EXPOSE 8765
CMD ["python", "-m", "web", "--demo", "--host", "0.0.0.0"]
