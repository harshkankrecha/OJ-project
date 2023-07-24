FROM python:3.9-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1



RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  && apt-get install -y python-lxml \
  # psycopg2 dependencies
  #&& apt-get install -y libpq-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt


COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

#ENV STATIC_ROOT=/static

COPY . .
RUN python manage.py collectstatic --no-input

# Copy the Nginx configuration file
#COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
# Collect static files
ENTRYPOINT [ "/entrypoint", "/start" ]
CMD [ "gunicorn","oj.wsgi:application","--bind", "0.0.0.0:8000" ]