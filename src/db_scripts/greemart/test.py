import json
import uuid
import psycopg2
from faker import Faker
import random
from random import randrange

connection = psycopg2.connect(
    host="localhost",
    database="greenmart",
    user="postgres",
    password="Sidhu@9693",
    gssencmode="disable"
)
fake = Faker('it_IT')
connection.autocommit = True

f = open('department.json', "r")
data = json.loads(f.read())
with connection.cursor() as cursor:
    for department in data:
        try:
            for k,category in data[department].items():
                print("key=",k)
                # print("cats=",category)
                # exit()
                try:
                    for sub_cat in category:
                        # print("sub_cat=",sub_cat)
                        # print("sub_cat name=",sub_cat['name'])
                        # print("sub_cat products=",sub_cat['products'])
                        # exit()
                        try:
                            for product in sub_cat['products']:
                                try:
                                    print("product-", product)
                                except Exception as sub_cat_err:
                                    print("product levele error:", sub_cat_err)
                        except Exception as cat_err:
                            print("sub_cat levele error:", cat_err)
                except Exception as second_err:
                    print("cat levele error:", second_err)

        except Exception as err:
            print("issue error addition =", err)
        print("Done !!!!")
    exit()
f.close()
