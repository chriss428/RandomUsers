FROM alpine:3.21.3 AS builder

WORKDIR /app

COPY req.txt .

RUN apk update && \
    apk add --no-cache \
    python3 \
    py3-pip \
    && rm -rf /var/cache/apk/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --upgrade pip && \
    pip install --no-cache-dir --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn -r req.txt

FROM builder

WORKDIR /app

COPY . .

CMD sh -c "sleep 5 && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"