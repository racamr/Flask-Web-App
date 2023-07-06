# MATCH MAKER ABROAD

Find your perfect international job!

WELCOME! This webapp code was forked from it's orginial repository. The purpose of this repository is to test the deployment via render. And it works!

## Business POV:
This webapp provides service for two types of users. For the explorers (users who apply for jobs) and companies (who post their jobs). Make note that this project is a functional protoype/demo and cnanot be used for real-time purposes. The webapp allows any sized company to post short term ( <12 months) oppurtunities fro backpack travellers or explorers, who can apply fro jobs efficiently with just one click. They submit their CV's effortlessly and find their company partner.

## Tech POV:
### Frotend
Bootstrap
HTML 
CSS
Javascript

### Backend
Flask
Python
NoSQL
Docker

### Database
MongoDB

### How to use the app:
When a new user or company signs in, please use these credentials to pay:

  Email: *any*

  Card number: 42424242424242

  MM/YY: *date in future*

  CVC: *any three digits*

  Zip code: *any*

### Running it locally and GitHub codespace:

#### Locally:
Run the app.py file and in your IDE terminal, crtl+click the local host link. The webapp will open on your browser.

Otherwise, in your IDE terminal, using Docker: In your terminal type execute/type these commands one after the other

1. docker build --tag python-docker .
2. docker run -p 5000:5000 python-docker

Now, you can open it on your browser from Docker Desktop or your IDE terminal.

#### GitHub codespace:
Create/start your codespace and after it loads, enter these commands in the codespace terminal:

1. docker build -t python-docker .
2. docker run -p 5000:5000 python-docker

Now, go to "ports" (next to terminal in your codespace) and click on the generated link under LOCAL ADRESS.

## Thankyou!
