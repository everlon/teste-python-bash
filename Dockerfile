FROM python:3.12.4
EXPOSE 5000
WORKDIR /api-uol
RUN mkdir api
RUN cd api/
COPY ./api/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "--app", "api/app", "run", "--host", "0.0.0.0", "--debug"]

# docker build -t uol-rest-api-flask-python .
# Usar --force-recreate para rebuild

# docker run -p 5000:5000 --name uol-teste -v .:/api-uol uol-rest-api-flask-python

# Não usarei WSGI Middleware no contexto de teste.
