import os, random, string, re, argparse, json
from webbrowser import get
from flask import Flask, request, jsonify
from flask_cors import CORS
from logging.config import dictConfig
from models.model import ManagementUser, ServiceUser

for dir in ["./logs"]:
    if not os.path.isdir(dir):
        os.mkdir(dir)

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    },
    'custom': {
        'class' : 'logging.handlers.TimedRotatingFileHandler',
        'formatter' : 'default',
        'filename' :'./logs/app.log'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'custom']
    }
})


UPLOAD_FOLDER = './uploaded_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
logger = app.logger
cors = CORS(app, resources={r"/uploads/*": {"origins": "*"}})
app.secret_key = '5fd470e8-3516-4e7c-bb5b-fce9c7984031'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_return_payload(status, message = "", data = None):
    return jsonify({"status": status, "message":message, "data" : data})

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def validateData(content_func):
    def inner(*args, **kwargs):
        logger.info("validating data")
        logger.info(f"Request method is : {request.method}")
        data = request.get_json()

        if "username" not in data:
            return "username not in data.", 404
        
        if "password" not in data:
            return "password not in data", 404

        if "email" in data:
            pass
        elif "mobile_number" in data:
            pass
        else:
            return "email or mobile number not in data.", 404

        return content_func(data)
    inner.__name__ = content_func.__name__
    return inner

def validatePassword(password):
    condition  = "Minimum eight characters, at least one letter and one number."
    regexFunction = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

    # Minimum eight characters, at least one letter, one number and one special character:
    # "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

    #Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:
    # "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"

    # Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
    # "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    # Minimum eight and maximum 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character:
    # "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,10}$"

    if re.match(regexFunction, password):
        return True, condition
    
    return False, condition

def authenticate(content_func):
    def inner(*args, **kwargs):
        logger.debug("authenticating")
        logger.debug(request.headers)
        if "USER-API-KEY" in request.headers and "USERNAME" in request.headers:
            user = ManagementUser.exists(request.headers.get("Username"), request.headers.get("User-Api-Key"))
            logger.info(user)
            if user:
                print("Authenticated!!")
                
            else:
                return "Unauthorized", 401
        else:
            return "Unauthorized", 401
        return content_func(*args, **kwargs)
    inner.__name__ = content_func.__name__
    return inner

def is_validApiKey(username, apikey):
    return True

@app.route('/fm/', methods = ['GET'])
def home():
    return "File uploader engine v0.001"

@app.route('/fm/admin/login/', methods = ['POST'])
def adminLogin():
    headers = request.headers
    data = request.get_json()

    if not 'username' in data:
        return get_return_payload(False, "Username not given",)

    username = data.get('username')

    if not 'password' in data:
        return get_return_payload(False, "Password not given.")
    
    password = data.get('password')

    user = ManagementUser.login(username, password)
    if user:
        return get_return_payload(True, "Logged in", data = user)
    return get_return_payload(False, message = "No such user or unauthorized.")

    # if not 'apikey' in headers:
    #     return get_return_payload(False, "Api key not given.")

    # apikey = data.get('apikey')
    # if not is_validApiKey(username, apikey):
    #     return get_return_payload(False, "Api key expired. Login again.")

@app.route('/fm/login/', methods = ['POST'])
def login():

    headers = request.headers
    data = request.get_json()
    payload = {}
    payload["validation_type"] = "password"

    if not 'username' in data:
        return get_return_payload(False, "Username not given",)

    username = data.get('username')

    if not 'password' in data:
        return get_return_payload(False, "Password not given.")
    
    password = data.get('password')
    
    user = ServiceUser.login(username, password)

    if user:
        payload.update(user)
        return get_return_payload(True, "Logged in", data = payload)

    return get_return_payload(False, message = "No such user or unauthorized.", data = payload)

@app.route('/fm/isValid/', methods = ['POST'])
def validateAPIKey():
    headers = request.headers
    data = request.get_json()
    payload = {}
    payload["validation_type"] = "api_key"
    

    if not 'username' in data:
        return get_return_payload(False, "Username not given",)

    username = data.get('username')

    if not 'api_key' in data:
        return get_return_payload(False, "ApiKey not given.")
    
    apiKey = data.get('api_key')
    
    user = ServiceUser.exists(username, apiKey)
    if user:
        return get_return_payload(True, "API Key Valid", data = payload)
    return get_return_payload(False, message = "Invalid API Key", data = payload)

@app.route('/fm/register/', methods = ['POST'])
def create_user():
    def formatify(ob):
        ob = json.loads(json.dumps(dict(ob.__dict__), default=str))
        ob.pop('id')
        ob.pop('_sa_instance_state')
        return ob

    headers = request.headers
    data = request.get_json()

    if not 'username' in data:
        return get_return_payload(False, "Username not given",)

    username = data.get('username')

    if not 'password' in data:
        return get_return_payload(False, "Password not given.")
    
    password = data.get('password')

    if not 'email' in data:
        return get_return_payload(False, "Email not given.")
    
    email = data.get('email')

    user = ServiceUser()
    user.username = username
    user.password_hash = password
    user.email = email

    uid = user.create()


    payload = formatify(user.get('single',uid))

    return get_return_payload(True, "Login Success", data = payload)

@app.route('/fm/uploads', methods=['GET', 'POST'])
def upload_file():
    print(request.method)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return get_return_payload(False, "Filepart not found.")

        uploaded_files = request.files.getlist('file')

        if not uploaded_files:
            return get_return_payload(False, "No files to upload.")
        
        for f in uploaded_files:
            original_filename =  f.filename
            print(f"Got file: {original_filename}.")
            print("Saving file.")
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], original_filename))

        return get_return_payload(True, "Upload Success")
    else:
        return '''
            <!doctype html>
                <head>
                    <title>Upload new File</title>
                    <h1>Upload new File</h1>
                </head>
                <body>
                    <form method=post enctype=multipart/form-data>
                        <label for = "upload_file">Select a file:</label>
                        <input id = "upload_file" type=file name=file multiple>
                        <input type=submit value=Upload>
                    </form>
                </body>
            </html>
        '''

if __name__ == '__main__':
    PORT = 5050
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--PORT', help = "port to run", default = PORT)
    args = parser.parse_args()

    logger.info("Starting server on port 5050.")
    app.run(host='0.0.0.0', port=args.PORT, debug=True)
