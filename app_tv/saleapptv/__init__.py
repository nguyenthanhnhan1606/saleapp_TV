from flask import  Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_babelex import Babel


cloudinary.config(cloud_name='dc8bwsbud',
                  api_key='437178481642573',
                  api_secret='SNlnGLzz5wPA7huH1IISdaAFF-4')


app = Flask(__name__)
app.secret_key = '$%^*&())(*&%^%4678675446&#%$%^&&*^$&%&*^&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/it01saletvdb?charset=utf8mb4' % quote('admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY_1'] = 'cart_1'

db = SQLAlchemy(app=app)

babel = Babel(app=app)


login = LoginManager(app=app)


@babel.localeselector
def load_locale():
    return 'vi'

