# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /python-docker

COPY requirement.txt requirement.txt 
RUN pip3 install --no-cache-dir -r requirement.txt 

COPY . .

EXPOSE 5000

#CMD ["python3", "app.py"]

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
