FROM python:3.10-slim
WORKDIR /app
COPY . .
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y locales software-properties-common gcc wget curl tzdata libsndfile1  \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install uvicorn[standard]
