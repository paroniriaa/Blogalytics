First, clone the repository  
  `git clone https://github.com/cs130-w21/15.git`  
Second, setup the virtual environment
 ```
 $ pip install virtualenv // if you haven't installed virtualenv before
 $ virtualenv 15 
 $ source 15/bin/activate
 ```
Third, go to the downloaded folder and run server
 ```
 $ cd 15 
 $ pip3 install -r requirements.txt
 $ python3 manage.py makemigrations
 $ python3 manage.py migrate
 $ python3 manage.py createsuperuser  
 $ python3 manage.py runserver 
 ```
Then, in your browser, enter `localhost:8000`  

 ## Lisence
[Apache-2.0](https://github.com/cs130-w21/15/blob/master/LICENSE)

 
