import db from '../../app.py'


class UsersModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(), primary_key=True)
    job = db.Column(db.String())
    company = db.Column(db.String())
    ssn = db.Column(db.Integer())
    residence = db.Column(db.String())
    blood_group = db.Column(db.String())
    website = db.Column(db.String())
    username = db.Column(db.String())
    name = db.Column(db.String())
    sex = db.Column(db.String())
    address = db.Column(db.String())
    mail = db.Column(db.String())
    birthdate = db.Column(db.Date())
    assigned_to = db.Column(db.String())
    created_by = db.Column(db.String())
   def __init__(self, user_id,job,company,ssn,residence,blood_group,website,username,name,sex,address,mail,birthdate,assigned_to,created_by):
         self.user_id = user_id,
         self.job =job,
         self.company =company,
         self.ssn =ssn,
         self.residence =residence,
         self.blood_group =blood_group,
         self.website =website,
         self.username =username,
         self.name =name,
         self.sex =sex,
         self.address =address,
         self.mail =mail,
         self.birthdate =birthdate,
         self.assigned_to =assigned_to,
         self.created_by =created_by

    def __repr__(self):
        return f"<Users {self.name}>"



user = api.model('Users', {
    'user_id': fields.String(required=True, description='cars'),
    'job': fields.String(required=True, description='cars'),
    'company': fields.String(required=True, description='cars'),
    'ssn': fields.String(required=True, description='cars'),
    'blood_group': fields.String(required=True, description='cars'),
    'website': fields.String(required=True, description='cars'),
    'username': fields.String(required=True, description='cars'),
    'name': fields.String(required=True, description='cars'),
    'sex': fields.String(required=True, description='cars'),
    'address': fields.String(required=True, description='cars'),
    'mail': fields.String(required=True, description='cars'),
    'birthdate': fields.String(required=True, description='cars'),
    'assigned_to': fields.String(required=True, description='cars'),
    'created_by': fields.String(required=True, description='cars'),
    'residence': fields.String(required=True, description='residence')
})
