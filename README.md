# Bloom SERVE

To have a running local database, here are the steps to follow : 
- Install dependencies from the `pyproject.toml`file
- From the `docker` folder, run `docker compose up` to run db & pgadmin containers
- From the project root, run `alembic upgrade head` to apply all migrations and have the schema populating the local db.
Some env variables will need to be exported : 
```
export POSTGRES_HOSTNAME=localhost
export POSTGRES_DB=serve
export POSTGRES_PASSWORD=bloom
export POSTGRES_USER=bloom_user
export POSTGRES_PORT=5480
```

To launch the API locally, here is the procedure : 
- Install the repo locally with `pip install -e .`
- Launch the server with uvicorn : `uvicorn app:app --reload`
- Find the Swagger documentation on http://localhost:8000/docs 
- Ingest initial list of MEPs in base, using the `create_batch_meps` route