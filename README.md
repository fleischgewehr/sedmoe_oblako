# Flask Cloud Storage

Upload, set lifecycle and share your files.

#### Requirements

App was made with Flask and PostgreSQL as storage. If you want to run it locally,
you should have PostgreSQL Server installed.

First of all, create new Python virtual environment, activate it and install
all needed packages by typing into bash:
    
    pip install -r requirements.txt
    
## Usage

To upload a file, go to home page and fill in all the fields with next requirements:

* file name must be in latin letters and less than 50 characters
* expiration hours must be greater or equal than 1
* file size must be less than 3 mb
* permitted extensions are txt, pdf, png, jpg, jpeg or gif

If you was not redirected to the new page after submitting a file,
 your input is invalid.

![alt text](https://gifmaker.me/files/download/home/20190505/01/ryTSg8rI3ucg5pTEZj5GQ4/output_EX24Jr.gif)

You can use this app either authorized or not. Logged users can check their files
at profile section. If file has no owner, it will be lost forever in case if
user lost its link.

#### Expiration specifics

Submitted expiration time will be rounded to hours (time like XX:00). Be aware 
of it when uploading new files.

#### Running locally

As was said before, you should have PostgreSQL Server running on your local
machine and all the packages from `requirements.txt` installed. If you're
running on linux, type 

    export SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:port/database
    export SECRET_KEY=YOUR_SECRET_KEY
    
Otherwise, set environment variables in way it is supposed to be done in your OS.

Run Python in project root directory, type `from evocloud import db` and 
initialize tables by entering `db.create_all()`. Now run Flask application
and enjoy yourself.