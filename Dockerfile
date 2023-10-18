FROM python:3 as dependencies
WORKDIR /test
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

FROM dependencies as run
COPY . .
ENTRYPOINT [ "python", "index.py" ]