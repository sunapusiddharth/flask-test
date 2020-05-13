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
        # add department
        dept_id = str(uuid.uuid4())
        deptObject = {
            "id": dept_id,
            "name": department,
            "veg": random.random() < 0.7,
            "adult": random.random() < 0.7
        }
        try:
            cursor.execute('''
                INSERT INTO department VALUES (
                    %(id)s,
                    %(name)s,
                    %(veg)s,
                    %(adult)s
                );
            ''', {
                **deptObject,
            })
            for k,category in data[department].items():
                cat_id = str(uuid.uuid4())
                catObject = {
                    "id": cat_id,
                    "name": k,
                    "dept_id": dept_id
                }
                try:
                    cursor.execute('''
                    INSERT INTO category VALUES (
                        %(id)s,
                        %(name)s,
                        %(dept_id)s
                    );
                ''', {
                        **catObject,
                    })
                    for sub_cat in category:
                        subcat_id = str(uuid.uuid4())
                        subcatObject = {
                            "id": subcat_id,
                            "dept_id": dept_id,
                            "cat_id": cat_id,
                            "name": sub_cat['name']
                        }
                        try:
                            cursor.execute('''
                            INSERT INTO sub_category VALUES (
                                %(id)s,
                                %(dept_id)s,
                                %(cat_id)s,
                                %(name)s
                            );
                            ''', {
                                **subcatObject,
                            })

                            for product in sub_cat['products']:
                                product_id = str(uuid.uuid4())
                                months = []
                                for _ in range(randrange(10)):
                                    months.append(fake.month())
                                months = list(dict.fromkeys(months))
                                productObject = {
                                    "id": product_id,
                                    "name": product['name'],
                                    "description": fake.paragraph(),
                                    "months": months,
                                    "promo_code": [],
                                    "dept_id": dept_id,
                                    "cat_id": cat_id,
                                    "discount": [],
                                    "brand": '',
                                    "brand_page": '',
                                    "qty_variant": product['qty_variant'],
                                    "price": product['price'],
                                    "sub_cat_id": subcat_id,
                                    "image": [product['image']]
                                }
                                try:
                                    cursor.execute('''
                                    INSERT INTO product VALUES (
                                        %(id)s,
                                        %(name)s,
                                        %(description)s,
                                        %(months)s,
                                        %(promo_code)s,
                                        %(dept_id)s,
                                        %(cat_id)s,
                                        %(discount)s,
                                        %(brand)s,
                                        %(brand_page)s,
                                        %(qty_variant)s,
                                        %(price)s,
                                        %(sub_cat_id)s,
                                        %(image)s
                                    );
                                    ''', {
                                        **productObject,
                                    })
                                    print("dept-", deptObject)
                                    print("cat-", catObject)
                                    print("sub_cat-", subcatObject)
                                    print("product-", productObject)
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
