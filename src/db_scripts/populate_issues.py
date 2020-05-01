import uuid
from faker import Faker
import json
import datetime
import psycopg2
import csv
import os
import random
cwd = os.path.dirname('../data/Consumer_Complaints.csv')
fake = Faker('it_IT')
connection = psycopg2.connect(
    host="localhost",
    database="news",
    user="postgres",
    password="Sidhu@9693",
    gssencmode="disable"
)
connection.autocommit = True

issues = [None] * 1000
out = os.path.abspath(os.path.join('../../data/', 'Consumer_Complaints.csv'))
print("cwd=", out)
# Helper fns:


def as_array(l):
    l2str = ','.join('"{}"'.format(x) for x in l)
    return '{{{}}}'.format(l2str)


# Read csv:
# Row
# OrderedDict([('Date received', '3/27/2012'),
#  ('Product', 'Credit card'), ('Sub-product', ''),
#  ('Issue', 'Billing disputes'), ('Sub-issue', ''),
#  ('Consumer complaint narrative', ''), ('Company public response', ''),
#  ('Company', 'WELLS FARGO & COMPANY'),
#  ('State', 'MA'), ('ZIP code', '1507'),
#  ('Tags', ''),
#  ('Consumer consent provided?', 'N/A'),
#  ('Submitted via', 'Referral'), ('Date sent to company', '3/28/2012'), ('Company response to consumer', 'Closed without relief'), ('Timely response?', 'Yes'), ('Consumer disputed?', 'No'), ('Complaint ID', '42126')])
with open(out, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    added_count = 0
    error_count = 0
    for row in reader:
        # print(row)
        user_id = str(uuid.uuid4())
        created_date = str(fake.date())
        clients = ['Johnson & johnson', 'pfizer', 'merck & co',
                   'baxter', 'Abott', 'General Electric', 'Web Md']
        issue_type = ['Delivery', 'Payment', 'Invoice',
                      'Health Plan', 'Product', 'Sales', 'App Performance']
        submitted_via = ['Web', 'App']
        issueObject = {
            "id": user_id,
            "assigned_to":[],
            "docs": [],
            "created_date": created_date,
            "product": row['Product'],
            "sub_product": row['Sub-product'],
            "issue_title": row['Issue'],
            "sub_issue": row['Sub-issue'],
            "issue_desc": row['Consumer complaint narrative'] if row['Consumer complaint narrative'] != '' else fake.paragraph(2),
            "response": row['Company public response'] if row['Company public response'] != '' else fake.paragraph(2),
            "company": row['Company'],
            "submitted_via": random.choice(submitted_via),
            "timely_response": row['Timely response?'],
            "client": random.choice(clients),
            "created_by":[],
            "type": random.choice(issue_type)
        }
        # print("userObject=", issueObject)
        with connection.cursor() as cursor:
            try:
                # print(cursor.mogrify('''
                #     INSERT INTO issues VALUES (
                #         %(id)s,
                #         %(assigned_to)s,
                #         %(docs)s,
                #         %(created_date)s,
                #         %(product)s,
                #         %(sub_product)s,
                #         %(issue_title)s,
                #         %(sub_issue)s,
                #         %(issue_desc)s,
                #         %(response)s,
                #         %(company)s,
                #         %(submitted_via)s,
                #         %(timely_response)s,
                #         %(client)s,
                #         %(created_by)s,
                #         %(type)s
                #     );
                # ''', {
                #     **issueObject
                # }))
                cursor.execute('''
                    INSERT INTO issues VALUES (
                       %(id)s,
                        %(assigned_to)s,
                        %(docs)s,
                        %(created_date)s,
                        %(product)s,
                        %(sub_product)s,
                        %(issue_title)s,
                        %(sub_issue)s,
                        %(issue_desc)s,
                        %(response)s,
                        %(company)s,
                        %(submitted_via)s,
                        %(timely_response)s,
                        %(client)s,
                        %(created_by)s,
                        %(type)s
                    );
                ''', {
                    **issueObject
                })
                print("issue added !!!")
                added_count +=1
            except Exception as err:
                print("issue error addition =", err)
                error_count+=1
print("All Done recordcount=",added_count,"error count",error_count)       

# with connection.cursor() as cursor:
#     for issue in issueObjects:
#         try:
#             issue['issue_id'] =  str(issue['issue_id'])
#             issue['birthdate'] =  str(issue['birthdate'])
#             print(issue['birthdate'])
#             cursor.execute('''
#                 INSERT INTO issues VALUES (
#                     %(issue_id)s,
#                     %(job)s,
#                     %(company)s,
#                     %(ssn)s,
#                     %(residence)s,
#                     %(blood_group)s,
#                     %(website)s,
#                     %(issuename)s,
#                     %(name)s,
#                     %(sex)s,
#                     %(address)s,
#                     %(mail)s,
#                     %(birthdate)s
#                 );
#             ''', {
#                 **issue
#             })
#             print("issue added !!!")
#         except Exception as err:
#             print("issue error addition =", err)
# print("All issues added !!!")
# # f.write(issueObjects)
# f.close()
# print("COmpleted !!!!")
