FROM python:3.10.7-slim-bullseye

WORKDIR /apps
COPY OfficeChat .
COPY requirements.dep requirements.dep
RUN pip install -r requirements.dep

WORKDIR /OfficeChat

# Run your Python application
CMD [ "python3", "run.py" ]



