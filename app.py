from flask import Flask, request, make_response, jsonify
import dbhelpers, apihelpers, dbcreds

app = Flask(__name__)

@app.post("/api/pokemon")
def post_pokemon():
    error = apihelpers.check_endpoint_info(request.json, ["name", "description", "image_url"])
    if(error != None):
        return make_response(jsonify(error), 400)
    
    results = dbhelpers.run_procedure('call insert_pokemon(?,?,?)', 
                            [request.json.get("name"),request.json.get("description"),request.json.get("image_url")])
    
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response("Sorry, there has been an error", 500)
    
@app.get("/api/pokemon")
def get_paintings():
    results = dbhelpers.run_procedure('call get_pokemon()', [])
    
    if(type(results) == list):
        return make_response(jsonify(results), 200)
    else:
        return make_response("Sorry, there has been an error", 500)

if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Development Mode")
    app.run(debug=True)