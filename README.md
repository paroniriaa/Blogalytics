## Porject Intro:
I corporate with teammates to design, implement, test, and maintain a web blog platform which integrated with analytic tools such as NLP in machine learning to generate unique text visualization image(word cloud) for each blog to empower users to preview its content by its word cloud; and frontend mouse tracker to capture user behaviors on the blog page then produce behavioral heatmap to help user better analysis its reader’s preference. 


## Porject Summary:
• I am heavily responsible for developing the frontend and backend of the web application infrastructure along with the automatic testing, such as views and GUI elements on every HTML page, and most of the fundamental backend blog platform functionality including but not limited to: pages of home, about, user profile; post, search, view, edit, and delete blogs.

• Strictly followed certain software architecture during the application development: N-Tier for the application landscape pattern to enable tier independent development; CQRS for the application structure pattern due to more frequent reads than writes; MVC for user interface pattern for the faster development process and multi-views delivery.

• Adapted agile software development methodologies and formed scrum team with a weekly sprint to establish strong, close, daily cooperation between the cross-functional team that works in: analysis, planning, design, coding, unit testing, and acceptance discussion, which ensured continuous demand-oriented code to be delivered during each sprint and quickly adapt to changes/new demands for next sprint.


## Build instructions

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
 $ pip3 install spacy==2.3.5    
 $ pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.0/en_core_web_sm-2.3.0.tar.gz
 $ pip3 install -r requirements.txt
 $ python3 manage.py makemigrations
 $ python3 manage.py migrate
 $ python3 manage.py createsuperuser  
 $ python3 manage.py runserver 
 ```
Then, in your browser, enter `localhost:8000`  

 ## Lisence
[Apache-2.0](https://github.com/cs130-w21/15/blob/master/LICENSE)

 
