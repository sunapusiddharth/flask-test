import uuid
from faker import Faker
import json
import datetime
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="news",
    user="postgres",
    password="Sidhu@9693",
    gssencmode="disable"
)
connection.autocommit = True

users = [None] * 10000

print("users=",len(users))
def as_array(l):
    l2str = ','.join('"{}"'.format(x) for x in l)
    return '{{{}}}'.format(l2str)


f = open("users.json", "a")
fake = Faker('it_IT')
userObjects = []
for user in users:
    user_id = uuid.uuid4()
    profile = fake.profile()
    userObject = {}
    for x in profile:
        if x != 'current_location':
            userObject[x] = profile[x]
    userObject["user_id"] = user_id
    # print("Single object=", userObject)
    userObjects.append(userObject)
print("userObjects=",len(userObjects))
with connection.cursor() as cursor:
    for user in userObjects:
        try:
            cursor.execute('''SELECT id from issues where random() < 0.01 limit 1;''')
            random_created_by = cursor.fetchone()[0]
            cursor.execute('''SELECT id from issues where random() < 0.01 limit 3;''')
            random_assigned_to = list(cursor.fetchone())
            print("random_created_by=",random_created_by)
            print("random_assigned_to=",random_assigned_to)
            user['user_id'] =  str(user['user_id'])
            user['birthdate'] =  str(user['birthdate'])
            user['assigned_to'] =  random_assigned_to
            user['created_by'] =  random_created_by
            print(user['birthdate'])
            cursor.execute('''
                INSERT INTO users VALUES (
                    %(user_id)s,
                    %(job)s,
                    %(company)s,
                    %(ssn)s,
                    %(residence)s,
                    %(blood_group)s,
                    %(website)s,
                    %(username)s,
                    %(name)s,
                    %(sex)s,
                    %(address)s,
                    %(mail)s,
                    %(birthdate)s,
                    %(assigned_to)s,
                    %(created_by)s
                );
            ''', {
                **user
            })
            print("user added !!!")
        except Exception as err:
            print("user error addition =", err)
print("All users added !!!")
# f.write(userObjects)
f.close()
print("COmpleted !!!!")


# def create_staging_table(cursor) -> None:
#     cursor.execute("""
#         DROP TABLE IF EXISTS staging_beers;
#         CREATE UNLOGGED TABLE staging_beers (
#             id                  INTEGER,
#             name                TEXT,
#             tagline             TEXT,
#             first_brewed        DATE,
#             description         TEXT,
#             image_url           TEXT,
#             abv                 DECIMAL,
#             ibu                 DECIMAL,
#             target_fg           DECIMAL,
#             target_og           DECIMAL,
#             ebc                 DECIMAL,
#             srm                 DECIMAL,
#             ph                  DECIMAL,
#             attenuation_level   DECIMAL,
#             brewers_tips        TEXT,
#             contributed_by      TEXT,
#             volume              INTEGER
#         );
#     """)

#     with connection.cursor() as cursor:
#      create_staging_table(cursor)
