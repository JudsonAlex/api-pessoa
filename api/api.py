from flask import Flask
from controllers.pessoa_controller import bp_pessoa


app = Flask(__name__)
app.register_blueprint(bp_pessoa, url_prefix='/pessoa')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)