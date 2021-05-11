# syntax=docker/dockerfile:1
# Haalt de base image op (python 3.8 image)
FROM python:3.8-slim-buster

# Zet de juiste environment variables
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements.txt naar de image
COPY requirements.txt requirements.txt
# Installeer de dependencies
RUN pip3 install -r requirements.txt

# Voeg de source code toe aan de image
COPY . .

# Command dat uitgevoerd wordt bij het starten van de image ("python ./main.py")
CMD [ "python", "./htmlparser/parser.py" ]