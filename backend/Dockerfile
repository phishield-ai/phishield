# First stage: Build stage
FROM python:3.11-slim as build_stage

WORKDIR /phishield/

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential python3-dev libffi-dev libcurl4-openssl-dev libssl-dev gcc curl git && \
    rm -rf /var/lib/apt/lists/*

RUN pip install hatch

COPY pyproject.toml ./
COPY phishield ./phishield

RUN hatch build

# Second stage: Runtime stage
FROM python:3.11-slim

COPY --from=build_stage /phishield/dist/phishield*.whl /tmp/

RUN addgroup phishield && \
    adduser --disabled-password --gecos "" --ingroup phishield phishield && \
    pip install --no-cache-dir /tmp/phishield*.whl && \
    rm -rf /tmp/phishield*.whl

USER phishield

WORKDIR /phishield


ENTRYPOINT ["phishield"]

EXPOSE 8000