FROM ghcr.io/astral-sh/uv:python3.13-alpine

RUN mkdir /app
WORKDIR /app


COPY . .

RUN uv sync --locked --no-dev

EXPOSE 80

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "pygrader-web.py", "--server.port=80", "--server.address=0.0.0.0"]