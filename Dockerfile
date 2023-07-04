# Используем базовый образ Python
FROM python:3.11.2

# Копируем requirements.txt в контейнер
COPY requirements.txt /app/

# Установка библиотек в зависимостях
RUN pip install --upgrade setuptools


RUN apt-get update && apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget \
      python3-tk && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости

RUN mkdir /src
WORKDIR /src
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install libzbar0 -y && pip install pyzbar

# Копируем исходный код в контейнер
COPY . /app
WORKDIR /app

# Запускаем бот
CMD ["python", "bot.py"]
