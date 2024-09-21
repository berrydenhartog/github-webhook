ARG PYTHON_VERSION=3.12-slim

FROM --platform=$BUILDPLATFORM python:${PYTHON_VERSION}

LABEL maintainer=berrydenhartog \
    organization=berrydenhartog \
    license=MIT \
    org.opencontainers.image.description="Github webhook event processor" \
    org.opencontainers.image.source=https://github.com/berrydenhartog/github-webhook \
    org.opencontainers.image.licenses=MIT

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/github_webhook
EXPOSE 8000
CMD ["uvicorn", "github_webhook.main:app", "--host", "0.0.0.0", "--app-dir", "/app/", "--port", "8000", "--no-server-header"]
