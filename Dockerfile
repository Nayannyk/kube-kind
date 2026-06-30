FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN grep -v futures requirements.txt > req-nofutures.txt && \
    pip install --no-cache-dir -r req-nofutures.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--threads", "25", "main:app"]
