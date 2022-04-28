FROM python:3.8-slim-buster
# FROM python:3.8-buster

WORKDIR /a/team/fighting/madup/love

RUN python -m pip install --upgrade pip
COPY requirements.txt .

# pakages required for setting up WSGI and others
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev default-libmysqlclient-dev

RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn","madup.wsgi:application","--bind","0.0.0.0"]