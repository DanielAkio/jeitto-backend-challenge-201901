from app import app
import os

os.environ['MYSQL_URI'] = 'mysql://root:password@localhost:3306/jeitto'
os.environ['SECRET_KEY'] = 'secret_key'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
