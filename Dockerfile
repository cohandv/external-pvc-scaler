FROM python

WORKDIR /app
COPY src .

RUN pip install -r requirements.txt

CMD python /app/main.py

