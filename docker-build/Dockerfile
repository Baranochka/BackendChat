FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock prestart.sh ./

RUN uv sync --frozen --no-cache

COPY fastapi-chat ./fastapi-chat

RUN chmod +x prestart.sh

ENTRYPOINT [ "./prestart.sh" ]

CMD ["uv", "run", "fastapi-chat/main.py"]