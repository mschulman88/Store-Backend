from bottle import route, run, template, static_file, get, post, delete, request
from sys import argv
import json
import pymysql

# CONNECT TO THE DATABASE
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='********!',
                             db='store',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


# CREATING A CATEGORY
@post("/category")
def create_category(name):
    new_category = request.POST.get("name")

    if new_category == " ":
        return json.dumps({"STATUS": "ERROR",
                           "MSG": "Bad Request",
                           "CAT_ID": None,
                           "CODE": 400})
    else:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT name FROM category"
                cursor.execute(sql)
                categories = cursor.fetchall()

                for category in categories:
                    if new_category == category[""]:
                        return json.dumps({"STATUS": "ERROR",
                                           "MSG": "Category Already Exists",
                                           "CAT_ID": None,
                                           "CODE": 200})

                sql = "INSERT INTO category VALUES(id, %s)"
                category_name = new_category
                cursor.execute(sql, category_name)
                id_new_category = cursor.lastrowid
                connection.commit()
                return json.dumps({"STATUS": "SUCCESS",
                                   "MSG": "Category Created Successfully",
                                   "CAT_ID": id_new_category,
                                   "CODE": 201})

        except:
            return json.dumps({"STATUS": "ERROR",
                               "MSG": "Internal error",
                               "CAT_ID": None,
                               "CODE": 500})


# DELETING A CATEGORY
@route("/category/<id>", method='DELETE')
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM category WHERE id = {}".format(id)
            cursor.execute(sql)
            connection.commit()
            return json.dumps({"STATUS": "SUCCESS",
                               "MSG": "Category Deleted Succesfully",
                               "CODE": 201})

    except:
        return json.dumps({'STATUS': 'ERROR',
                           'MSG': "Internal error",
                           "CODE": 500})


# STATIC ROUTES
@get("/admin")
def admin_portal():
    return template("pages/admin.html")


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=7000)
