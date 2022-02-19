# tech-blog
# description
- Blog site can post, read, update articles
- Using flask,jinja2, postgresql, alembic
# Clone 

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

# Some images
## REGISTER  
![image](https://user-images.githubusercontent.com/43593736/154785350-38a0306d-fe41-4e19-9e4b-7b080fc0dea6.png)  
## LOGIN  
![image](https://user-images.githubusercontent.com/43593736/154785317-d354dd51-29a4-4bd3-b551-32d45a4b57a6.png)  
## CREATE NEW POST  
![image](https://user-images.githubusercontent.com/43593736/154785363-fea234fc-e6f8-4f9b-8c3b-d9f8a40cd113.png)  
## SHOW ALL POST  
![image](https://user-images.githubusercontent.com/43593736/154785000-587bf2b6-97f7-414b-95b7-c9a255c20041.png)  
## SHOW POST AFTER SEARCH  
![image](https://user-images.githubusercontent.com/43593736/154785218-1eb1f36b-4646-48ca-b5f8-a04ec6a38a32.png)  
## SHOW POST IN SIMILAR TAG  
![image](https://user-images.githubusercontent.com/43593736/154785229-b8e69fef-2863-4ae7-81e6-5b7e72c512f7.png)  
## PROFILE  
![image](https://user-images.githubusercontent.com/43593736/154785357-9897c350-18e6-405f-b590-f15c0b50b56a.png)  
## EDIT MY POST  
![image](https://user-images.githubusercontent.com/43593736/154785375-5b223432-b93e-4f45-9564-589bd58ee07e.png) 
