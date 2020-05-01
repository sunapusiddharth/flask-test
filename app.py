from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.exceptions import BadRequest
import './src/routes/users.py'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Sidhu@9693@localhost:5432/news?gssencmode=disable"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Car {self.name}>"


app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
          description='A simple TodoMVC API',
          )

ns = api.namespace('todos', description='TODO operations')
cs = api.namespace('cars', description='Cars operations')

todo = api.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})

car = api.model('Car', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'name': fields.String(required=True, description='cars'),
    'model': fields.String(required=True, description='cars'),
    'doors': fields.Integer(required=True, description='cars'),
})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)

# Cars :
@cs.route('/')
class CarsList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @cs.doc('list_cars')
    # @cs.marshal_list_with(cars)
    def get(self):
        '''List all cars'''
        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]
        print("cars=", results)
        return results, 200

    @cs.doc('create_car')
    @cs.expect(car)
    # @cs.marshal_with(car, code=201)
    def post(self):
        '''Create a new car'''
        data = api.payload
        try:
            new_car = CarsModel(
            name=data['name'], model=data['model'], doors=data['doors'])
            db.session.add(new_car)
            db.session.commit()
            return {"message": f"car {new_car.name} has been created successfully."},201
        except:
            raise BadRequest('My custom message')

# Operations on /
@cs.route('/<int:id>')
@cs.response(404, 'car not found')
@cs.param('id', 'The task identifier')
class Car(Resource):
    '''Show a single car item and lets you delete them'''
    @ns.doc('get_car')
    # @ns.marshal_with(car)
    def get(self, id):
        '''Fetch a given resource'''
        print("GET id",id)
        car = CarsModel.query.get_or_404(id)
        print("GET cR",car)
        response = {
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return {"message": "success", "car": response}

    @ns.doc('delete_car')
    @ns.response(204, 'car deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        car = CarsModel.query.get_or_404(id)
        db.session.delete(car)
        db.session.commit()
        return {"message": f"Car {car.name} successfully deleted."},204

    @ns.expect(car)
    # @ns.marshal_with(car)
    def put(self, id):
        '''Update a car given its identifier'''
        car = CarsModel.query.get_or_404(id)
        data = api.payload
        car.name = data['name']
        car.model = data['model']
        car.doors = data['doors']
        db.session.add(car)
        db.session.commit()
        return {"message": f"car {car.name} successfully updated"}



# Users route:
# swagger
users_swagger = api.namespace('users', description='users operations')

if __name__ == '__main__':
    app.run(debug=True)
