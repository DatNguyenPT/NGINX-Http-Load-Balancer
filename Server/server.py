from flask import Response, Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import os
import time


app = Flask(__name__)

_INF = float("inf")

graphs = {}
graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))

# Set the server ID from environment variable
server_id = os.getenv('SERVER_ID', 'Unknown')

# Read the database URL from environment variable
db_url = os.getenv('DATABASE_URL')

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/')
def home():
    start = time.time()
    graphs['c'].inc()
    time.sleep(0.600)
    end = time.time()
    graphs['h'].observe(end - start)

    return f'This is server {server_id}'

@app.route("/metrics")
def requests_count():
    res = []
    for k,v in graphs.items():
        res.append(prometheus_client.generate_latest(v))
    return Response(res, mimetype="text/plain")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
