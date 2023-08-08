FROM python:3.10.7-slim-bullseye

WORKDIR /apps

COPY requirements.dep requirements.dep
RUN pip install -r requirements.dep
COPY OfficeChat .

# Run your Python application
CMD [ "python3", "run.py" ]



