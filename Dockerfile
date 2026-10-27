FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai \
    PORT=8000

WORKDIR /app

RUN groupadd -r app && useradd -r -g app -u 10001 app \
    && chown app:app /app

COPY --chown=app:app main.py server.py index.html README.md ./

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=2)"

CMD ["python", "server.py"]
