
## Installation and Usage
The user is recommended to use poetry to run this project.
Docker is also required as this project creates a postgres instance in a docker container.

Connection details are as follows - it is recommended that the user accesses the data using a client e.g. DBeaver, to view the data.

Host: localhost

User: postgres

Password: password

To install all the required dependencies and ensure pre-commit is installed, run:

```bash
poetry install
 
pre-commit install
   
```

## Why you chose this schema/approach
I chose this schema as it allowed checking for both primary key and foreign key violations. 
It also means that we don't get bogged down with possible varied data in JSON form.

## Alternative approaches you considered

I considered using a DynamoDB table (this can be ran in a docker container) but thought against it because of the lack of join capabilities.

## Trade-offs in terms of performance, cost, and scalability

This uses Postgres and SQLalchemy - sqlalchemy can be a bit slow on inserts. Postgres is still one of the best tools for transactional data and although it can be costly it is a predictable cost.
Analytic work might be better suited in Snowflake for fast but expensive querying. Some people use Snowflake for transactional purposes but this is controversial.
Postgres will handle high volumes of traffic but DynamoDB might be better suited due to its more reactive throughput.

## How you would handle additional data sources (e.g., listening events)

Postgres would still be a brilliant tool for additional sources. 
Could have Airflow instance for orchestrated jobs, ECS for API related jobs or lambda for simple triggered jobs.


## Troubleshooting

Some IDEs, such as PyCharm, may struggle to identify modules elsewhere in this repository. Make sure to mark the `src` directory as 'Sources Root' by right-clicking the folder and selecting `Mark Directory as Sources Root`.

## Testing

Pytest has been used for testing - this generates a testing docker container which runs the tests in a separate docker container to that created in src/main.py

```bash
pytest
    
```