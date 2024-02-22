# This Dockerfile builds a custom Python container. It installs dependencies, sets the work directory,
# copies a file from the local directory into the Docker container, and sets the entrypoint for running the copied
# Python script.

FROM python:3.9.1

RUN apt-get update && apt-get install -y wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY hw1-ingestion-pipeline.py hw1-ingestion-pipeline.py 

ENTRYPOINT [ "python", "hw1-ingestion-pipeline.py" ]
