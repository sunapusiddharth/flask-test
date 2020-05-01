import api from '../../app.py'
import UserModel from '../model/users.py'


class Users(object):
    def __init__(self):
        self.user_id = '',
        self.job = '',
        self.company = '',
        self.ssn = '',
        self.residence = '',
        self.blood_group = '',
        self.website = [],
        self.username = '',
        self.name = '',
        self.sex = '',
        self.address = '',
        self.mail = '',
        self.birthdate = '',
        self.assigned_to = [],
        self.created_by = ''

    # def get(self, id):

    #     api.abort(404, "Todo {} doesn't exist".format(id))
    def listAll(self, skip, limit):
        users = UsersModel.query.all()
        return users, 200
    # def create(self, data):
    #     todo = data
    #     todo['id'] = self.counter = self.counter + 1
    #     self.todos.append(todo)
    #     return todo

    # def update(self, id, data):
    #     todo = self.get(id)
    #     todo.update(data)
    #     return todo

    # def delete(self, id):
    #     todo = self.get(id)
    #     self.todos.remove(todo)
