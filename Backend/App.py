#User Ziyang Zhang
#Restful-API
#2020/05/11


from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

##Import AUR-Labor-Data
Labdata = pd.read_csv('./AURData/Labour.csv')


@app.route('/', methods=['GET'])
def home():
    return "<h1>Group25 Data API</h1><p>This site is a prototype API for Tweet Data.</p>"

@app.route('/Labordata', methods=['GET'])
def get_labor():
    return Labdata.to_json()

def abort_if_todo_nexit(todo_id):
    if todo_id not in TODOS:
        abort(404, message = "not exit")

##add json file value
parser = reqparse.RequestParser()
parser.add_argument('task')

##del/put one value
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_nexit(todo_id)
        return TODO[todo_id]

## post.get all data
class TodoList(Resource):
    def get(self):
        return TODOS

#set Api
api.add_resource(TodoList, '/todos')
api.add_resource(Todo,'/todos/<todo_id>')    

if __name__ == '__main__':
    app.run(debug=True)