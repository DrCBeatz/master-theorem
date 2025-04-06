# handler.py

from mangum import Mangum
from backend.main import app

handler = Mangum(app)

def run(event, context):
    return handler(event, context)
