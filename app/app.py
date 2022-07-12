from flask import Flask, request, jsonify
from flask_cors import CORS
from openastrochart.openAstroChart import openAstroChart
import json

app = Flask(__name__)
CORS(app)
app.debug = True
@app.route('/')
def hello_world():
    return 'Web Service for OpenAstro v1.1.57'


@app.route('/createchart/', methods=['GET', 'POST'])
def createchart() :
    oac   = request.json
    print ('createchart - creating openAstroChart')
    chart = openAstroChart ()
    print ('createchart - importing JSON string to openAstroChart')
    chart.setChartData (oac)
    print ('createchart - calc chart')
    chart.calc ()
    print ('createchart - convert chart back to JSON and return')
    chart_JSON = chart.getChartToJSON ()
    return jsonify(chart_JSON)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    