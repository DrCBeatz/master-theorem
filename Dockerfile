# Dockerfile

FROM python:3.10.4-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Expose the port server is running on
EXPOSE 8000

# Start the server
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]