# Gera a imagem
FROM python:3.11.9-alpine

LABEL maintainer="leonardolucasbs"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 1) Pacotes de sistema necessários para psycopg2, lxml, Pillow, etc.
RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    linux-headers \
    jpeg-dev zlib-dev libjpeg-turbo-dev \
    libffi-dev openssl-dev \
    curl bash

# 2) Pastas
WORKDIR /djangoapp
COPY djangoapp /djangoapp
COPY scripts /scripts
RUN sed -i 's/\r$//' /scripts/*.sh 2>/dev/null || true \
    && chmod -R +x /scripts
SHELL ["/bin/sh", "-c"]

# 3) Virtualenv
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip

# 4) Instala deps Python
#    (seu requirements.txt fica em /djangoapp/requirements.txt)
RUN /venv/bin/pip install -r /djangoapp/requirements.txt

# 5) Usuário sem privilégios
RUN adduser -D -H -s /sbin/nologin duser && \
    mkdir -p /data/web/static /data/web/media && \
    chown -R duser:duser /venv /data/web /djangoapp /scripts && \
    chmod -R 755 /data/web/static /data/web/media && \
    chmod -R +x /scripts

# 6) PATH p/ venv e scripts
ENV PATH="/scripts:/venv/bin:${PATH}"

# 7) Porta do app
EXPOSE 8000

# 8) Muda user
USER duser

# 9) Comando de entrada
#    IMPORTANTE: seu scripts/commands.sh precisa ter shebang correto.
CMD ["commands.sh"]
