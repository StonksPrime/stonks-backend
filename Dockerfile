FROM python:3-alpine

# Project Files and Settings
RUN mkdir -p code
WORKDIR /code

# Copy project
COPY . /code/

#COPY Pipfile Pipfile.lock ./
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


# Server
EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
