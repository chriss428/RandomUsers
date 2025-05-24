FROM alpine:3.21.3 AS builder

WORKDIR /app

COPY req.txt .

RUN apk update && \
    apk add --no-cache \
    python3 \
    py3-pip \
    && rm -rf /var/cache/apk/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r req.txt

FROM builder

WORKDIR /app

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]