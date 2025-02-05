FROM python:3.12.2-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client
COPY . .
CMD ["uvicorn", "src.main:app", "--reload", "--host=0.0.0.0"]