from app import app
import os

os.environ['MYSQL_URI'] = 'uri'
os.environ['SECRET_KEY'] = 'secret_key'

if __name__ == '__main__':
    app.run(debug=True)
