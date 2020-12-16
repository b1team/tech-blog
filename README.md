# tech-blog

`git clone https://github.com/b1team/tech-blog.git && cd tech-blog`  

## Installing dependencies
`pip install -r requirements.txt`  

## Configuration
1. `cp .env.template .env`  
2. `vim .env` and add required configurations

## Database migration
1. Run `export PYTHONPATH=$PWD`  
2. `cd ./src`  
3. `alembic upgrade head`  

## Run
1. In `tech-blog` folder, run `export PYTHONPATH=$PWD`  
2. run `python src/main.py`  

# Development
1. Upgrade models, migrating models  
In `src` folder, run `alembic revision --autogenerate -m "<your change logs>"`  
And run `alembic upgrade head` to upgrade your database with latest models
