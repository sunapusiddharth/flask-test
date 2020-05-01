from '../../app.py' import users_swagger 
from '../model/users.py' import UsersModel,user
from '../controller/UsersController.py' import Users

@users_swagger.route('/')
class UsersList(Resource):
    '''Shows a list of all users, and lets you POST to add new user'''
    @users_swagger.doc('users_doc')
    @users_swagger.marshal_list_with(user)
    def get(self):
        '''List all tasks'''
        return Users.listAll()

    # @users_swagger.doc('create_todo')
    # @users_swagger.expect(todo)
    # @users_swagger.marshal_with(todo, code=201)
    # def post(self):
    #     '''Create a new task'''
    #     return DAO.create(api.payload), 201


# @users_swagger.route('/<int:id>')
# @users_swagger.respousers_swaggere(404, 'Todo not found')
# @users_swagger.param('id', 'The task identifier')
# class Todo(Resource):
#     '''Show a single todo item and lets you delete them'''
#     @users_swagger.doc('get_todo')
#     @users_swagger.marshal_with(todo)
#     def get(self, id):
#         '''Fetch a given resource'''
#         return DAO.get(id)

#     @users_swagger.doc('delete_todo')
#     @users_swagger.respousers_swaggere(204, 'Todo deleted')
#     def delete(self, id):
#         '''Delete a task given its identifier'''
#         DAO.delete(id)
#         return '', 204

#     @users_swagger.expect(todo)
#     @users_swagger.marshal_with(todo)
#     def put(self, id):
#         '''Update a task given its identifier'''
#         return DAO.update(id, api.payload)
