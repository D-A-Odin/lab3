FROM python:3.11

WORKDIR app

COPY . .

ENV w "{2, 7, 11, 21, 42, 89, 180, 354}"
ENV message "Hello World!"

RUN pip install -r requirements.txt

CMD ["python", "main.py"]