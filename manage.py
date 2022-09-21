from flask_script import Manager, Server
from app import inicializar_app
from config import config

configuracion = config['development']
app = inicializar_app(configuracion)

manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port=8000))

if __name__ == '__main__':
    manager.run()
# python .\manage.py runserver