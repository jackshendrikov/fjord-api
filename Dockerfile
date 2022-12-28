FROM python:3.10-slim

RUN mkdir /code
WORKDIR /code

COPY requirements.txt requirements-prod.txt piccolo_conf.py version.py ./

RUN pip install -U pip
RUN pip install -r requirements-prod.txt

ENV PYTHONPATH "${PYTHONPATH}:/main"

COPY main main/

# Expose ports
EXPOSE 5000

CMD ["uvicorn", "main.app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
