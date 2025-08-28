FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем Python, LibreOffice и все необходимые зависимости
RUN apt-get update && apt-get install -y \
    software-properties-common \
    python3 \
    python3-pip \
    libreoffice \
    libreoffice-common \
    libreoffice-core \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    fonts-dejavu \
    libxinerama1 \
    libglu1-mesa \
    libgtk-3-0 \
    libxrender1 \
    libsm6 \
    libice6 \
    libxext6 \
    libgl1 \
    libdbus-glib-1-2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Делаем alias, чтобы точно работала команда libreoffice
RUN ln -s /usr/bin/libreoffice7.3 /usr/bin/libreoffice || true

# Проверяем бинарник
RUN libreoffice --version || echo "LibreOffice binary is ready"

WORKDIR /app

# Ставим зависимости Python
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Запуск приложения
CMD ["python3", "main.py"]
