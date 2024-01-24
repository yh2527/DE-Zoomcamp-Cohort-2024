FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY hw1-ingestion-pipeline.py hw1-ingestion-pipeline.py 

ENTRYPOINT [ "python", "hw1-ingestion-pipeline.py" ]
