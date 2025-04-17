FROM python:3.10

ENV PYTHONBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on


RUN apt update && apt upgrade -y && apt install -y build-essential libssl-dev
RUN pip install "setuptools<58.0.0"
RUN pip install cmake --no-cache-dir --prefer-binary

WORKDIR /app

# Remove .git folder before copying built files
RUN rm -rf .git

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "roadstone_project.wsgi"]
