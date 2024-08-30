# Job matching
Job matching is a simple application that shows matching job of a person considering his/her skills and experience

## Installing
### For development
Requirements:
- python 3.11 or higher
- postgres 16 or higher
- virtualenv installed

Activate virtualenv (supposing the name of virtualenv is venv)
- with windows
```bash
    venv/Scripts/activate
```
- with Mac or Linux
```bash
    source venv/bin/activate
```

Then you can install dependencies
```bash
    pip install -r requirements.txt
```

Copy .env.example to an .env file and configure all the variable and run the migration command

```bash
    python manage.py migrate
```

To seed the database with data (you only need to run this one time)

```bash
    python manage.py seed
```

Now you are good to go

### With docker
You can easily run a production mode with docker. You just have to configure the .env file. For that, don't forget to set the DB_HOST to db (it's the name of the database service in the docker compose). You can set the other variables whaterver you want it.

```env
    DB_HOST=db
```

Now, you just run the container with this command

```bash
    docker compose up --build
```

If you want it in detach mode

```bash
    docker compose up --build -d
```

To seed the database with data, the container should be running

```bash
    docker exec job-matching python manage.py seed
```