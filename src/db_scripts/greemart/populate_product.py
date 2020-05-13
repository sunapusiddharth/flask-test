import uuid
from faker import Faker
import json
import datetime
import psycopg2
import csv
import os
import random
from random import randrange
fake = Faker('it_IT')
connection = psycopg2.connect(
    host="localhost",
    database="greenmart",
    user="postgres",
    password="Sidhu@9693",
    gssencmode="disable"
)
connection.autocommit = True

issues = [None] * 1000
out = os.path.abspath(os.path.join('../../../data/', 'products.csv'))
print("cwd=", out)
# Helper fns:

def as_array(l):
    l2str = ','.join('"{}"'.format(x) for x in l)
    return '{{{}}}'.format(l2str)


with open(out, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    added_count = 0
    error_count = 0
    for row in reader:
        with connection.cursor() as cursor:
            # cursor.execute(
            #     '''SELECT id from department where random() < 0.01 limit 1;''')
            # random_dept_id = cursor.fetchone()[0]
            dept_id = str(uuid.uuid4())
            months = []
            for _ in range(randrange(10)):
                months.append(fake.month())
            months = list(dict.fromkeys(months))
            deptObject = {
                "id": row['product_id'],
                "name": row['product_name'],
                "description": fake.paragraph(),
                "months": months,
                "promo_code": [],
                "dept_id": row['department_id'],
                "cat_id": row['aisle_id'],
                "discount": [],
            }
            try:
                # print(cursor.mogrify('''
                #     INSERT INTO product VALUES (
                #         %(id)s,
                #         %(name)s,
                #         %(description)s,
                #         %(months)s,
                #         %(promo_code)s,
                #         %(dept_id)s,
                #         %(cat_id)s,
                #         %(discount)s
                #     );
                # ''', {
                #     **deptObject,
                # }))
                # exit()
                cursor.execute('''
                    INSERT INTO product VALUES (
                        %(id)s,
                        %(name)s,
                        %(description)s,
                        %(months)s,
                        %(promo_code)s,
                        %(dept_id)s,
                        %(cat_id)s,
                        %(discount)s
                    );
                ''', {
                    **deptObject,
                })
                print("issue added !!!")
                added_count += 1
            except Exception as err:
                print("issue error addition =", err)
                error_count += 1
print("All Done recordcount=", added_count, "error count", error_count)
