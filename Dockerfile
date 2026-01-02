FROM ghcr.io/astral-sh/uv:python3.13-alpine

RUN mkdir /app
WORKDIR /app


COPY . .

RUN uv sync --locked --no-dev

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["uv", "run", "main.py"]