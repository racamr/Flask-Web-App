# File to run when we want to start the web server

from Website import create_app

app = create_app()
if __name__ == '__main__':
    app.run( debug=True)