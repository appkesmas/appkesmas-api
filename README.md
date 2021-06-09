# appkesmas-api

Implementating REST API using django web framework for commmucation in the backend and mobile appes. Also this api delivering machine learning model for waiting time prediction and giving hospital recommendation.

## How to Run

```bash
### Run backend api server

# clone appkesmas-api repository
git clone https://github.com/appkesmas/appkesmas-api
cd appkesmas-api

# create python environment
sudo apt instal python3-venv
python3 -m venv venv
source venv/bin/activate

# install django library
pip3 install -r requirements.txt

# migrate database
python3 manage.py migrate

# run development server
python3 manage.py runserver 0.0.0.0:8000

### Run static files using container

# install docker
sudo apt install -y docker.io

# enter to asset directory
cd appkesmas-api/assets

# run nginx container and expose to http port
sudo docker run --name nginx --rm -dit -p 80:80 -v ${PWD}:/usr/share/nginx/html/static nginx
```

## API Docs

Appkesmas API Documentation : [https://documenter.getpostman.com/view/16163677/TzY7fEVU](https://documenter.getpostman.com/view/16163677/TzY7fEVU)
