# jev-bot runs on the standard library only, so the image is just Python.
# Build:  docker build -t jev-bot .
# Run:    docker run --rm jev-bot decisions
#         docker run --rm jev-bot card BTC
#         docker run --rm -e TYPESAFE_API_KEY=... jev-bot decisions --engine jev
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .

ENTRYPOINT ["python", "-m", "jev_bot"]
CMD ["decisions"]
