FROM python:3.10-slim

WORKDIR /app

COPY . .

SHELL ["/bin/bash", "-c"]

RUN python -m venv venv && \
    source "venv/bin/activate" && \
    pip install \
    --no-cache-dir \
    --requirement "requirements.txt"

RUN chmod +x run_web_server.sh

EXPOSE 8090

CMD ["./run_web_server.sh"]
