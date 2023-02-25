FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install https://test.pypi.org/simple/tdei-gtfs-csv-validator
COPY ./src /code/src
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]