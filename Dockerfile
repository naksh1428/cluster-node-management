FROM python:3.9-alpine
LABEL authors="akshatap"

WORKDIR /src

COPY requirement.txt /src/requirenment.txt
RUN pip install --upgrade pip
RUN pip install -r /src/requirenment.txt


COPY ./app /src/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host","0.0.0.0","--port", "8000"]