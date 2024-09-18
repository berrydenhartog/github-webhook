ARG PYTHON_VERSION=3.12-slim

FROM --platform=$BUILDPLATFORM python:${PYTHON_VERSION}

LABEL maintainer=berrydenhartog \
    organization=berrydenhartog \
    license=MIT \
    org.opencontainers.image.description="Github to mattermost webhook" \
    org.opencontainers.image.source=https://github.com/berrydenhartog/github-mattermost \
    org.opencontainers.image.licenses=MIT

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app/mattermost_github
EXPOSE 8000
CMD ["uvicorn", "mattermost_github.main:app", "--host", "0.0.0.0", "--app-dir", "/app/", "--port", "8000"]
