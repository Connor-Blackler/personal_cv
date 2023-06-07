# Dockerfile
FROM python:3.11
WORKDIR /usr/src/app

COPY . .

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

RUN chmod +x /usr/src/app/entrypoint.sh

# specify the port number the container should expose
EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
