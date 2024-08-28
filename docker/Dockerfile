FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY ./otus_final_project .

RUN pip install -r requirements.txt

RUN sed -i 's/\r$//g' docker-build/start && chmod +x docker-build/start

