### Steps to run:
Python version requirements:
```Python 3.10```

Development Environment: Ubuntu 22.04 LTS or WSL running Ubuntu 22.04

1.) Install docker and docker compose via apt `sudo apt install docker docker-compose`

2.) Copy the sample.env to app.env `cp sample.env app.env`

3.) Run `docker compose build`

4.) Run `docker compose up -d`

5.) If the setup is successful, open http://localhost/admin on your browser

6.) To run migrations `docker compose exec web python3 manage.py migrate`

7.) To create superuser `docker compose exec web python3 manage.py createsuperuser`

#### To check for logs

`docker compose logs -f <service_name>`

example:

`docker compose logs -f web`

`docker compose logs -f celery`

`docker compose logs -f redis`
