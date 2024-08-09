from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import jwt
from functools import wraps
import configparser

# Load configuration from the config file
config = configparser.ConfigParser()
config.read('db_config.ini')

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = config['mysql']['host']
app.config['MYSQL_USER'] = config['mysql']['user']
app.config['MYSQL_PASSWORD'] = config['mysql']['password']
app.config['MYSQL_DB'] = config['mysql']['database']
app.config['SECRET_KEY'] = config['flask']['secret_key']

mysql = MySQL(app)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            token = token.split(" ")[1]  # Remove "Bearer " prefix
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 403
        return f(*args, **kwargs)
    return decorator

@app.route('/api/login', methods=['POST'])
def login():
    auth = request.json
    username = auth.get('username')
    password = auth.get('password')

    if username == 'admin' and password == 'password':
        token = jwt.encode({'user': username}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/highTrafficIPs', methods=['GET'])
@token_required
def get_high_traffic_ips():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM high_traffic_ips")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

@app.route('/api/protocolUsage', methods=['GET'])
@token_required
def get_protocol_usage():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM protocol_usage")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

@app.route('/api/anomalies', methods=['GET'])
@token_required
def get_anomalies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM anomalies")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

@app.route('/api/ipClusters', methods=['GET'])
@token_required
def get_ip_clusters():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ip_clusters")
    result = cur.fetchall()
    cur.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)