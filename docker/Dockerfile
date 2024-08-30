FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY . .

RUN pip install -r requirements.txt

COPY ./docker/start.sh /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

