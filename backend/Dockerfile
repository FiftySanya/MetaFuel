FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && \ pip install -r requirements.txt

COPY . /app

ENV DJANGO_SETTINGS_MODULE=django_back.settings

EXPOSE 8000

CMD ["gunicorn", "--workers", "3", "django_back.wsgi:application", "--bind", "0.0.0.0:8000"] 