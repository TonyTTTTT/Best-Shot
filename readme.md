# BestShot
- BestShot is a Social Media where you can upload your post your picture on it for sharing with each other.
- The novelty compare to other Social Media is that we embed an Convolutional Neural Network(CNN) in it to score each picture user post.

## How to run
- Highly recommend to create a Python's virtual environment for this project, avoid from contaminate your native Python's environment.
```sh
# install the packages for create virtual environment
pip3 install virtualenv

# create virtual environment
cd Where/You/Want/To/Build/VirtualEnv
virtualenv BestShot

# activate virtual environment
# Windows
.\BestShot\Scripts\activate
# Linux
./BestShot/Scripts/acitvate
```
- This project is mainly developed in Python, so first you need to install all the requirement Python packages in "requirement.txt".
```sh
$ pip3 install -r requirement.txt
```
- We use Python Web framwork Django to build up this website, so after all requirement installed, just run the Django command to start the website.
```sh
$ cd /The/Path/of/BestShot
$ python3 manage.py runserver
```
- Then go to url: "http://127.0.0.1:8000/main/" in your browser, you will see the homepage of BestShot.