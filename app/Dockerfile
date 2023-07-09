FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN chmod a+x api/app.sh

CMD [ "python3", "main.py" ]