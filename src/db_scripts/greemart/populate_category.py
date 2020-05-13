import uuid
from faker import Faker
import json
import datetime
import psycopg2
import csv
import os
import random
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
out = os.path.abspath(os.path.join('../../../data/', 'aisles.csv'))
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
            deptObject = {
                "id": row['aisle_id'],
                "name": row['aisle'],
                # "dept_id": random_dept_id
            }
            try:
                # print(cursor.mogrify('''
                #     INSERT INTO category VALUES (
                #         %(id)s,
                #         %(name)s,
                #         %(dept_id)s
                #     );
                # ''', {
                #     **deptObject,
                # }))
                # exit()
                cursor.execute('''
                    INSERT INTO category VALUES (
                        %(id)s,
                        %(name)s
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
