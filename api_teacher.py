from flask import Flask
from flask_restful import Api, Resource, reqparse

from kuet_teacher_data import get_data

app = Flask(__name__)
api = Api(app)
data = get_data()

class Teacher_data(Resource):
    
    def get(self,id="CSE"):
        if(id=='ALL' or id=='all'):
            return data, 200
        for datac in data:
            if(datac==id):
                return data.get(datac),200
        return "Not Found",404


def contains(j,id):
    if(id in j.get("name").lower()):
        return True
    if(id in j.get("weblink").lower()):
        return True
    if(id in j.get("designation").lower()):
        return True
    if(id in j.get("image").lower()):
        return True
    if(id in j.get("phone").lower()):
        return True
    if(id in j.get("mail").lower()):
        return True
    return False;

class search_teacher(Resource):
    def get(self,id):
        ans = []
        id = id.lower()
        for datac in data:
            for j in data.get(datac):
                if(contains(j,id)):
                    ans.append(j)
        if(len(ans)>0):
            return ans,200
        return "Not Found",404

api.add_resource(Teacher_data,"/data","/data/","/data/<string:id>")
api.add_resource(search_teacher,"/find/<string:id>")

if __name__ == "__main__":
    app.run()

