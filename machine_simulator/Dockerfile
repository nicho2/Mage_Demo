FROM python:3

RUN mkdir demo
WORKDIR /demo
COPY machine_simulator/requirements.txt .
COPY machine_simulator/src .

RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python", "main.py" ]
