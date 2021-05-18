from flask import Flask
from flask_restful import reqparse, abort, Api, Resource,output_json
import pickle
import json

app = Flask(__name__)
api = Api(app)
api.app.config['RESTFUL_JSON'] = {
    'ensure_ascii': False
}
filename = '/kmean_model.sav'
model = pickle.load(open(filename, 'rb'))
f=open("/top_location.json")
data = json.load(f)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('long')
parser.add_argument('lat')
parser.add_argument('sys')

class PredictSentiment(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        longitude = args['long']
        latitude=args['lat']
        sys=args['sys']
        print(sys,longitude,latitude)
        output=[]
        if sys=='1':
            clus = model.predict(np.array([longitude, latitude]).reshape(1, -1))[0]

            for i in data:
                if i['cluster'] == clus:
                    output.append(i)
        return output



api.add_resource(PredictSentiment, '/')

if __name__ == '__main__':
    app.run(debug=True)
