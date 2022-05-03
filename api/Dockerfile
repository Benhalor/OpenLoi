FROM python:3.7-alpine
WORKDIR /api
ENV FLASK_APP=/api/app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]
