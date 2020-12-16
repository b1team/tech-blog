# tech-blog

`git clone https://github.com/b1team/tech-blog.git && cd tech-blog`  

## Installing dependencies
`pip install -r requirements.txt`  

## Configuration
1. `cp .env.template .env`  
2. Add required configurations

## Database migration
1. Run `export PYTHONPATH=$PWD`  
2. `cd ./src`  
3. `alembic upgrade head`  

## Run
1. In `tech-blog` folder, run `export PYTHONPATH=$PWD`  
2. run `python src/main.py`  
