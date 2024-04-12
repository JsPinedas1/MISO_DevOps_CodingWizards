FROM python:3.10

WORKDIR /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile
COPY . /app/
EXPOSE 3000
CMD FLASK_APP=/app/src/main.py pipenv run flask run -h 0.0.0.0 -p 3000