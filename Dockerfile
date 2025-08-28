FROM ubuntu:22.04

# Обновляем систему и ставим Python + LibreOffice + зависимости
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libreoffice \
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

# Ставим Python-пакеты
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Запуск приложения
CMD ["python3", "main.py"]