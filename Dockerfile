# FROM python:3.9

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# COPY requirements.txt .
# # install python dependencies
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt



FROM black_dash_appseed-app:latest

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# running migrations
# RUN python manage.py migrate

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]

# you have to run python manage.py migrate after gunicord run.
# it's means that you have to login to docker container and make migrations.